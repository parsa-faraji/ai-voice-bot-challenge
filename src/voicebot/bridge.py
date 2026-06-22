from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

from .artifacts import ArtifactStore
from .config import Settings
from .realtime import (
    connect_realtime,
    input_audio_append_event,
    response_cancel_event,
    response_create_event,
    session_update_event,
)
from .scenarios import Scenario, get_scenario


@dataclass
class BridgeState:
    run_id: str = "manual"
    call_sid: str = "unknown-call"
    stream_sid: str = ""
    scenario: Scenario | None = None
    start_time: float = 0.0
    session_configured: bool = False
    response_active: bool = False
    remote_media_seen: bool = False

    def elapsed(self) -> float:
        if not self.start_time:
            return 0.0
        return time.monotonic() - self.start_time


class MediaBridge:
    def __init__(self, settings: Settings, store: ArtifactStore):
        self.settings = settings
        self.store = store

    async def run(self, twilio_ws: WebSocket) -> None:
        await twilio_ws.accept()
        state = BridgeState(start_time=time.monotonic())
        async with connect_realtime(self.settings) as openai_ws:
            tasks = [
                asyncio.create_task(self._twilio_to_openai(twilio_ws, openai_ws, state)),
                asyncio.create_task(self._openai_to_twilio(twilio_ws, openai_ws, state)),
            ]
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            for task in done:
                task.result()

    async def _twilio_to_openai(self, twilio_ws: WebSocket, openai_ws: Any, state: BridgeState):
        try:
            while True:
                raw = await twilio_ws.receive_text()
                event = json.loads(raw)
                event_name = event.get("event")

                if event_name == "start":
                    await self._handle_start(event, openai_ws, state)
                    self._record(state, "twilio_in", event)
                elif event_name == "media":
                    self._record(state, "twilio_in", event)
                    state.remote_media_seen = True
                    payload = event.get("media", {}).get("payload")
                    if payload:
                        await openai_ws.send(json.dumps(input_audio_append_event(payload)))
                elif event_name == "stop":
                    self._record(state, "twilio_in", event)
                    break
                else:
                    self._record(state, "twilio_in", event)
        except WebSocketDisconnect:
            return

    async def _handle_start(self, event: dict[str, Any], openai_ws: Any, state: BridgeState) -> None:
        start = event.get("start", {})
        params = start.get("customParameters", {}) or {}
        scenario_id = params.get("scenario_id") or "appointment-simple"
        state.scenario = get_scenario(scenario_id)
        state.run_id = params.get("run_id") or state.run_id
        state.stream_sid = start.get("streamSid") or event.get("streamSid") or state.stream_sid
        state.call_sid = start.get("callSid") or state.call_sid

        await openai_ws.send(json.dumps(session_update_event(self.settings, state.scenario)))
        state.session_configured = True
        asyncio.create_task(self._delayed_initial_response(openai_ws, state))

    async def _delayed_initial_response(self, openai_ws: Any, state: BridgeState) -> None:
        await asyncio.sleep(self.settings.initial_greeting_delay_ms / 1000)
        if state.scenario and state.session_configured and not state.remote_media_seen:
            await openai_ws.send(json.dumps(response_create_event(state.scenario)))
            state.response_active = True

    async def _openai_to_twilio(self, twilio_ws: WebSocket, openai_ws: Any, state: BridgeState):
        async for raw in openai_ws:
            event = json.loads(raw)
            self._record(state, "openai_in", event)
            event_type = event.get("type")

            if event_type in {"response.output_audio.delta", "response.audio.delta"}:
                payload = event.get("delta") or event.get("audio")
                if payload and state.stream_sid:
                    await self._send_twilio_media(twilio_ws, state, payload)
                    state.response_active = True
            elif event_type == "input_audio_buffer.speech_started":
                await self._handle_barge_in(twilio_ws, openai_ws, state)
            elif event_type in {"response.done", "response.output_item.done"}:
                state.response_active = False
            elif event_type == "error":
                # Keep the call alive; errors are recorded in artifacts for debugging.
                state.response_active = False

    async def _send_twilio_media(
        self, twilio_ws: WebSocket, state: BridgeState, payload: str
    ) -> None:
        media_event = {
            "event": "media",
            "streamSid": state.stream_sid,
            "media": {"payload": payload},
        }
        await twilio_ws.send_text(json.dumps(media_event))
        mark_event = {
            "event": "mark",
            "streamSid": state.stream_sid,
            "mark": {"name": f"bot-audio-{int(state.elapsed() * 1000)}"},
        }
        await twilio_ws.send_text(json.dumps(mark_event))

    async def _handle_barge_in(self, twilio_ws: WebSocket, openai_ws: Any, state: BridgeState) -> None:
        if state.stream_sid:
            await twilio_ws.send_text(json.dumps({"event": "clear", "streamSid": state.stream_sid}))
        if state.response_active:
            await openai_ws.send(json.dumps(response_cancel_event()))
            state.response_active = False

    def _record(self, state: BridgeState, direction: str, event: dict[str, Any]) -> None:
        self.store.record_event(
            run_id=state.run_id,
            call_sid=state.call_sid,
            elapsed_seconds=state.elapsed(),
            direction=direction,
            event=event,
        )
