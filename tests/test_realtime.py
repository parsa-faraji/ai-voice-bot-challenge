from pathlib import Path

from voicebot.config import TARGET_TEST_NUMBER, Settings
from voicebot.realtime import input_audio_append_event, session_update_event
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


def test_legacy_session_update_can_be_selected():
    event = session_update_event(make_settings("legacy"), get_scenario("medication-refill"))
    assert event["session"]["input_audio_format"] == "g711_ulaw"
    assert event["session"]["output_audio_format"] == "g711_ulaw"


def test_audio_append_event_passes_twilio_payload_through():
    assert input_audio_append_event("abc123") == {
        "type": "input_audio_buffer.append",
        "audio": "abc123",
    }
