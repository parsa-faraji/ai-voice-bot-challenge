from pathlib import Path

import httpx

from voicebot.config import TARGET_TEST_NUMBER, Settings
from voicebot.diagnostics import validate_public_tunnel
from voicebot.scenarios import get_scenario
from voicebot.twiml import build_twiml


def settings(public_base_url: str = "https://abc.ngrok.app") -> Settings:
    return Settings(
        openai_api_key="sk-test",
        twilio_account_sid="AC123",
        twilio_auth_token="token",
        twilio_from_number="+13334445555",
        target_test_number=TARGET_TEST_NUMBER,
        public_base_url=public_base_url,
        artifacts_dir=Path("artifacts"),
    )


def test_public_tunnel_diagnostics_pass():
    app_settings = settings()
    scenario = get_scenario("appointment-simple")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/health":
            return httpx.Response(200, json={"status": "ok"})
        if request.url.path == "/twiml":
            return httpx.Response(
                200,
                text=build_twiml(app_settings, scenario, run_id="doctor"),
            )
        return httpx.Response(404)

    client = httpx.Client(transport=httpx.MockTransport(handler))

    checks = validate_public_tunnel(app_settings, scenario, client=client)

    assert all(check.ok for check in checks)


def test_public_tunnel_diagnostics_flags_http_and_bad_twiml():
    app_settings = settings("http://127.0.0.1:8000")
    scenario = get_scenario("appointment-simple")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/health":
            return httpx.Response(200, json={"status": "ok"})
        if request.url.path == "/twiml":
            return httpx.Response(200, text="<Response />")
        return httpx.Response(404)

    client = httpx.Client(transport=httpx.MockTransport(handler))

    checks = validate_public_tunnel(app_settings, scenario, client=client)

    assert [check.ok for check in checks] == [False, True, False]
