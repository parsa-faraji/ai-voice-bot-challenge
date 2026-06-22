from pathlib import Path
from xml.etree import ElementTree as ET

from voicebot.config import TARGET_TEST_NUMBER, Settings
from voicebot.scenarios import get_scenario
from voicebot.twiml import build_twiml


def test_build_twiml_uses_bidirectional_stream_without_query_params():
    settings = Settings(
        openai_api_key="sk-test",
        twilio_account_sid="AC123",
        twilio_auth_token="token",
        twilio_from_number="+13334445555",
        target_test_number=TARGET_TEST_NUMBER,
        public_base_url="https://abc.ngrok.app",
        artifacts_dir=Path("artifacts"),
    )
    xml = build_twiml(settings, get_scenario("appointment-simple"), "run-1")
    root = ET.fromstring(xml.removeprefix('<?xml version="1.0" encoding="UTF-8"?>'))
    stream = root.find("./Connect/Stream")
    assert stream is not None
    assert stream.attrib["url"] == "wss://abc.ngrok.app/media"
    assert "?" not in stream.attrib["url"]
    params = {node.attrib["name"]: node.attrib["value"] for node in stream.findall("Parameter")}
    assert params["scenario_id"] == "appointment-simple"
    assert params["run_id"] == "run-1"
