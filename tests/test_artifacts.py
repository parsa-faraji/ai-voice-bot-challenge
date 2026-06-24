import json

from voicebot.artifacts import TranscriptTurn, transcript_turn_from_openai_event, turns_from_event_file


def test_extracts_athena_agent_transcript_turn():
    turn = transcript_turn_from_openai_event(
        event={
            "type": "conversation.item.input_audio_transcription.completed",
            "transcript": "How can I help you today?",
        },
        elapsed_seconds=2.4,
    )
    assert turn is not None
    assert turn.speaker == "AthenaAgent"
    assert "help" in turn.text


def test_extracts_patient_bot_transcript_turn():
    turn = transcript_turn_from_openai_event(
        event={
            "type": "response.output_audio_transcript.done",
            "transcript": "I need to schedule an appointment.",
        },
        elapsed_seconds=5.0,
    )
    assert turn is not None
    assert turn.speaker == "PatientBot"


def test_rebuild_turns_from_event_file(tmp_path):
    path = tmp_path / "events.jsonl"
    entries = [
        {
            "elapsed_seconds": 1.2,
            "event": {
                "type": "response.output_audio_transcript.done",
                "transcript": "Hi there.",
            },
        },
        {
            "elapsed_seconds": 3.5,
            "event": {
                "type": "conversation.item.input_audio_transcription.completed",
                "transcript": "Thanks for calling.",
            },
        },
    ]
    path.write_text("\n".join(json.dumps(entry) for entry in entries), encoding="utf-8")
    turns = turns_from_event_file(path)
    assert [turn.speaker for turn in turns] == ["PatientBot", "AthenaAgent"]


def test_transcript_turn_format_collapses_internal_newlines():
    turn = TranscriptTurn(
        elapsed_seconds=54,
        speaker="PatientBot",
        text="Thanks, that helps.\n\nI have one more question.",
    )

    assert turn.format() == (
        "[00:54] PatientBot: Thanks, that helps. I have one more question."
    )


def test_transcript_turn_format_preserves_subsecond_timestamp():
    turn = TranscriptTurn(
        elapsed_seconds=96.4,
        speaker="AthenaAgent",
        text="Please hold.",
    )

    assert turn.format() == "[01:36.4] AthenaAgent: Please hold."
