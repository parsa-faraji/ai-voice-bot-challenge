from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CallRecord:
    run_id: str
    scenario_id: str
    call_sid: str
    to_number: str
    from_number: str
    status: str
    created_at: str


@dataclass(frozen=True)
class TranscriptTurn:
    elapsed_seconds: float
    speaker: str
    text: str

    def format(self) -> str:
        minutes = int(self.elapsed_seconds // 60)
        seconds = int(self.elapsed_seconds % 60)
        return f"[{minutes:02d}:{seconds:02d}] {self.speaker}: {self.text}"


class ArtifactStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.events_dir = self.root / "events"
        self.recordings_dir = self.root / "recordings"
        self.transcripts_dir = self.root / "transcripts"
        self.calls_path = self.root / "calls.jsonl"
        self.root.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)

    def append_call_record(self, record: CallRecord) -> None:
        with self.calls_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")

    def load_call_records(self) -> list[CallRecord]:
        if not self.calls_path.exists():
            return []
        records: list[CallRecord] = []
        for line in self.calls_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(CallRecord(**json.loads(line)))
        return records

    def event_path(self, run_id: str, call_sid: str) -> Path:
        safe_call_sid = call_sid or "unknown-call"
        return self.events_dir / f"{run_id}-{safe_call_sid}.jsonl"

    def record_event(
        self,
        *,
        run_id: str,
        call_sid: str,
        elapsed_seconds: float,
        direction: str,
        event: dict[str, Any],
    ) -> None:
        entry = {
            "ts": datetime.now(UTC).isoformat(),
            "elapsed_seconds": round(elapsed_seconds, 3),
            "direction": direction,
            "event": event,
        }
        with self.event_path(run_id, call_sid).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")

    def rebuild_transcripts(self) -> list[Path]:
        outputs: list[Path] = []
        for event_file in sorted(self.events_dir.glob("*.jsonl")):
            turns = turns_from_event_file(event_file)
            if not turns:
                continue
            output = self.transcripts_dir / f"{event_file.stem}.txt"
            header = [
                f"Call transcript: {event_file.stem}",
                "Speakers: PatientBot is this caller; AthenaAgent is the assessment target.",
                "",
            ]
            output.write_text("\n".join(header + [turn.format() for turn in turns]) + "\n")
            outputs.append(output)
        return outputs


def turns_from_event_file(path: Path) -> list[TranscriptTurn]:
    turns: list[TranscriptTurn] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        event = entry.get("event", {})
        turn = transcript_turn_from_openai_event(
            event=event,
            elapsed_seconds=float(entry.get("elapsed_seconds") or 0.0),
        )
        if turn:
            turns.append(turn)
    return turns


def transcript_turn_from_openai_event(
    *, event: dict[str, Any], elapsed_seconds: float
) -> TranscriptTurn | None:
    event_type = event.get("type", "")
    transcript = _extract_transcript(event)
    if not transcript:
        return None

    if event_type in {
        "conversation.item.input_audio_transcription.completed",
        "conversation.item.input_audio_transcription.done",
        "input_audio_transcription.completed",
        "input_audio_transcription.done",
    }:
        return TranscriptTurn(elapsed_seconds, "AthenaAgent", transcript)

    if event_type in {
        "response.output_audio_transcript.done",
        "response.audio_transcript.done",
    }:
        return TranscriptTurn(elapsed_seconds, "PatientBot", transcript)

    return None


def _extract_transcript(event: dict[str, Any]) -> str:
    direct = event.get("transcript")
    if isinstance(direct, str):
        return direct.strip()
    item = event.get("item")
    if isinstance(item, dict):
        for content in item.get("content", []):
            if isinstance(content, dict):
                text = content.get("transcript") or content.get("text")
                if isinstance(text, str) and text.strip():
                    return text.strip()
    response = event.get("response")
    if isinstance(response, dict):
        text = response.get("output_text")
        if isinstance(text, str):
            return text.strip()
    return ""
