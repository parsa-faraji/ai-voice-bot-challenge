from pathlib import Path

from fastapi.testclient import TestClient

from voicebot.config import TARGET_TEST_NUMBER, Settings
from voicebot.server import create_app


def test_health_and_twiml_routes():
    settings = Settings(
        openai_api_key="sk-test",
        twilio_account_sid="AC123",
        twilio_auth_token="token",
        twilio_from_number="+13334445555",
        target_test_number=TARGET_TEST_NUMBER,
        public_base_url="https://abc.ngrok.app",
        artifacts_dir=Path("artifacts"),
    )
    client = TestClient(create_app(settings))

    assert client.get("/health").json() == {"status": "ok"}
    response = client.get("/twiml", params={"scenario_id": "weekend-hours", "run_id": "test"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert "weekend-hours" in response.text
    assert "wss://abc.ngrok.app/media" in response.text
