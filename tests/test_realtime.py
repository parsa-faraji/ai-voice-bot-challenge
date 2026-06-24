from pathlib import Path

from voicebot.config import TARGET_TEST_NUMBER, Settings
from voicebot.realtime import input_audio_append_event, scenario_voice, session_update_event
from voicebot.scenarios import get_scenario


def make_settings(style: str = "ga") -> Settings:
    return Settings(
        openai_api_key="sk-test",
        twilio_account_sid="AC123",
        twilio_auth_token="token",
        twilio_from_number="+13334445555",
        target_test_number=TARGET_TEST_NUMBER,
        public_base_url="https://abc.ngrok.app",
        artifacts_dir=Path("artifacts"),
        realtime_session_style=style,
    )


def test_ga_session_update_contains_audio_and_scenario_instructions():
    event = session_update_event(make_settings(), get_scenario("medication-refill"))
    assert event["type"] == "session.update"
    assert "lisinopril" in event["session"]["instructions"]
    assert event["session"]["audio"]["input"]["format"]["type"] == "audio/pcmu"
    assert event["session"]["audio"]["output"]["format"]["type"] == "audio/pcmu"
    assert event["session"]["audio"]["output"]["voice"] == "cedar"


def test_legacy_session_update_can_be_selected():
    event = session_update_event(make_settings("legacy"), get_scenario("medication-refill"))
    assert event["session"]["input_audio_format"] == "g711_ulaw"
    assert event["session"]["output_audio_format"] == "g711_ulaw"
    assert event["session"]["voice"] == "cedar"


def test_scenario_voice_matches_patient_profile():
    settings = make_settings()

    assert scenario_voice(settings, get_scenario("appointment-simple")) == "marin"
    assert scenario_voice(settings, get_scenario("office-logistics")) == "cedar"


def test_session_update_uses_configured_vad_timing():
    settings = make_settings()
    settings = Settings(
        **{
            **settings.__dict__,
            "vad_threshold": 0.5,
            "vad_prefix_padding_ms": 400,
            "vad_silence_duration_ms": 950,
        }
    )

    event = session_update_event(settings, get_scenario("appointment-simple"))
    turn_detection = event["session"]["audio"]["input"]["turn_detection"]

    assert turn_detection["threshold"] == 0.5
    assert turn_detection["prefix_padding_ms"] == 400
    assert turn_detection["silence_duration_ms"] == 950


def test_audio_append_event_passes_twilio_payload_through():
    assert input_audio_append_event("abc123") == {
        "type": "input_audio_buffer.append",
        "audio": "abc123",
    }
