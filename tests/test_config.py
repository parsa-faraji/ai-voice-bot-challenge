from pathlib import Path

import pytest

from voicebot.config import (
    TARGET_TEST_NUMBER,
    ConfigError,
    TargetNumberError,
    assert_assessment_target,
    normalize_e164,
    public_http_to_ws,
)
from voicebot.config import Settings


def settings() -> Settings:
    return Settings(
        openai_api_key="sk-test",
        twilio_account_sid="AC123",
        twilio_auth_token="token",
        twilio_from_number="+13334445555",
        target_test_number=TARGET_TEST_NUMBER,
        public_base_url="https://example.ngrok.app",
        artifacts_dir=Path("artifacts"),
    )


def test_normalize_e164_us_number():
    assert normalize_e164("(805) 439-8008") == TARGET_TEST_NUMBER


def test_refuses_non_assessment_target():
    with pytest.raises(TargetNumberError):
        assert_assessment_target("+18054398009", settings())


def test_rejects_invalid_number():
    with pytest.raises(ConfigError):
        normalize_e164("not-a-number")


def test_public_http_to_ws_preserves_path():
    assert public_http_to_ws("https://abc.ngrok.app/base", "/media") == (
        "wss://abc.ngrok.app/base/media"
    )
