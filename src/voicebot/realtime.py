from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

import websockets

from .config import Settings
from .prompts import build_patient_instructions, opening_response_instruction
from .scenarios import Scenario


def realtime_url(settings: Settings) -> str:
    return f"wss://api.openai.com/v1/realtime?model={settings.realtime_model}"


@asynccontextmanager
async def connect_realtime(settings: Settings):
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "OpenAI-Safety-Identifier": "athena-voicebot-assessment",
    }
    url = realtime_url(settings)
    try:
        async with websockets.connect(url, additional_headers=headers) as websocket:
            yield websocket
    except TypeError:
        async with websockets.connect(url, extra_headers=headers) as websocket:
            yield websocket


def session_update_event(settings: Settings, scenario: Scenario) -> dict[str, Any]:
    style = settings.realtime_session_style.lower()
    if style == "legacy":
        return _legacy_session_update_event(settings, scenario)
    return {
        "type": "session.update",
        "session": {
            "type": "realtime",
            "instructions": build_patient_instructions(scenario),
            "output_modalities": ["audio"],
            "audio": {
                "input": {
                    "format": {"type": "audio/pcmu"},
                    "transcription": {"model": settings.transcription_model},
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.45,
                        "prefix_padding_ms": 350,
                        "silence_duration_ms": 650,
                        "create_response": True,
                        "interrupt_response": True,
                    },
                },
                "output": {
                    "format": {"type": "audio/pcmu"},
                    "voice": settings.realtime_voice,
                },
            },
            "reasoning": {"effort": "low"},
        },
    }


def _legacy_session_update_event(settings: Settings, scenario: Scenario) -> dict[str, Any]:
    return {
        "type": "session.update",
        "session": {
            "instructions": build_patient_instructions(scenario),
            "modalities": ["text", "audio"],
            "voice": settings.realtime_voice,
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "input_audio_transcription": {"model": settings.transcription_model},
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.45,
                "prefix_padding_ms": 350,
                "silence_duration_ms": 650,
                "create_response": True,
                "interrupt_response": True,
            },
        },
    }


def input_audio_append_event(payload_base64: str) -> dict[str, str]:
    return {"type": "input_audio_buffer.append", "audio": payload_base64}


def response_create_event(scenario: Scenario) -> dict[str, Any]:
    return {
        "type": "response.create",
        "response": {
            "instructions": opening_response_instruction(scenario),
            "modalities": ["audio"],
        },
    }


def response_cancel_event() -> dict[str, str]:
    return {"type": "response.cancel"}
