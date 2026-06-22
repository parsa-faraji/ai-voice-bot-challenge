from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import time
from uuid import uuid4

import httpx

from .artifacts import ArtifactStore, CallRecord
from .config import Settings, assert_assessment_target, require_live_call_settings
from .scenarios import Scenario


@dataclass(frozen=True)
class PlacedCall:
    run_id: str
    call_sid: str
    status: str
    scenario_id: str


TERMINAL_CALL_STATUSES = {"completed", "busy", "failed", "no-answer", "canceled"}


def place_assessment_call(
    *, settings: Settings, scenario: Scenario, store: ArtifactStore, run_id: str | None = None
) -> PlacedCall:
    require_live_call_settings(settings)
    assert_assessment_target(settings.target_test_number, settings)
    run_id = run_id or uuid4().hex[:10]

    from twilio.rest import Client

    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    url = f"{settings.twiml_url}?scenario_id={scenario.id}&run_id={run_id}"
    kwargs = {
        "to": settings.target_test_number,
        "from_": settings.twilio_from_number,
        "url": url,
        "method": "POST",
        "record": True,
        "recording_channels": "dual",
        "recording_track": "both",
        "time_limit": settings.max_call_seconds,
    }
    try:
        call = client.calls.create(**kwargs)
    except TypeError:
        kwargs.pop("recording_track", None)
        call = client.calls.create(**kwargs)

    record = CallRecord(
        run_id=run_id,
        scenario_id=scenario.id,
        call_sid=call.sid,
        to_number=settings.target_test_number,
        from_number=settings.twilio_from_number,
        status=getattr(call, "status", "created"),
        created_at=datetime.now(UTC).isoformat(),
    )
    store.append_call_record(record)
    return PlacedCall(
        run_id=run_id,
        call_sid=call.sid,
        status=getattr(call, "status", "created"),
        scenario_id=scenario.id,
    )


def wait_for_call_completion(
    *, settings: Settings, call_sid: str, poll_seconds: int = 5, timeout_seconds: int | None = None
) -> dict[str, str | None]:
    require_live_call_settings(settings)
    from twilio.rest import Client

    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    timeout = timeout_seconds or settings.max_call_seconds + 90
    deadline = time.monotonic() + timeout
    last_status = None
    while time.monotonic() < deadline:
        call = client.calls(call_sid).fetch()
        last_status = getattr(call, "status", None)
        if last_status in TERMINAL_CALL_STATUSES:
            return {
                "status": last_status,
                "duration": getattr(call, "duration", None),
                "error_code": getattr(call, "error_code", None),
                "error_message": getattr(call, "error_message", None),
            }
        time.sleep(poll_seconds)
    return {
        "status": last_status or "unknown",
        "duration": None,
        "error_code": "timeout",
        "error_message": f"Call did not complete within {timeout} seconds.",
    }


def download_recordings(settings: Settings, store: ArtifactStore) -> list[Path]:
    require_live_call_settings(settings)
    from twilio.rest import Client

    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    downloaded: list[Path] = []
    for record in store.load_call_records():
        recordings = client.recordings.list(call_sid=record.call_sid, limit=10)
        for recording in recordings:
            output = store.recordings_dir / f"{record.run_id}-{record.scenario_id}-{recording.sid}.mp3"
            if output.exists():
                downloaded.append(output)
                continue
            content = _download_recording_mp3(settings, recording.sid, requested_channels=2)
            output.write_bytes(content)
            downloaded.append(output)
    return downloaded


def _download_recording_mp3(
    settings: Settings, recording_sid: str, requested_channels: int
) -> bytes:
    base = (
        f"https://api.twilio.com/2010-04-01/Accounts/"
        f"{settings.twilio_account_sid}/Recordings/{recording_sid}.mp3"
    )
    auth = (settings.twilio_account_sid, settings.twilio_auth_token)
    with httpx.Client(timeout=60) as client:
        response = client.get(base, params={"RequestedChannels": requested_channels}, auth=auth)
        if response.status_code == 400 and requested_channels == 2:
            response = client.get(base, params={"RequestedChannels": 1}, auth=auth)
        response.raise_for_status()
        return response.content
