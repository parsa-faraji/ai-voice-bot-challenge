from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

TARGET_TEST_NUMBER = "+18054398008"


class ConfigError(ValueError):
    """Raised when required runtime configuration is missing or unsafe."""


class TargetNumberError(ConfigError):
    """Raised when code attempts to call any number except the assessment line."""


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str
    target_test_number: str
    public_base_url: str
    artifacts_dir: Path
    realtime_model: str = "gpt-realtime-2"
    realtime_voice: str = "marin"
    realtime_female_voice: str = "marin"
    realtime_male_voice: str = "cedar"
    realtime_session_style: str = "ga"
    analysis_model: str = "gpt-5.5"
    transcription_model: str = "gpt-4o-transcribe"
    initial_greeting_delay_ms: int = 1200
    initial_audio_ignore_ms: int = 8000
    vad_threshold: float = 0.45
    vad_prefix_padding_ms: int = 350
    vad_silence_duration_ms: int = 850
    run_suite_spacing_seconds: int = 45
    max_call_seconds: int = 180

    @property
    def twiml_url(self) -> str:
        base = self.public_base_url.rstrip("/")
        return f"{base}/twiml"

    @property
    def stream_url(self) -> str:
        return public_http_to_ws(self.public_base_url, "/media")

    @property
    def stream_status_url(self) -> str:
        base = self.public_base_url.rstrip("/")
        return f"{base}/stream-status"


def load_settings(env_file: str | Path | None = ".env") -> Settings:
    if env_file:
        load_dotenv(resolve_env_file(env_file))

    target = normalize_e164(os.getenv("TARGET_TEST_NUMBER", TARGET_TEST_NUMBER))
    if target != TARGET_TEST_NUMBER:
        raise TargetNumberError(
            f"TARGET_TEST_NUMBER must be {TARGET_TEST_NUMBER}; got {target!r}."
        )

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
        twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
        twilio_from_number=normalize_e164(os.getenv("TWILIO_FROM_NUMBER", "")),
        target_test_number=target,
        public_base_url=os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:8000"),
        artifacts_dir=Path(os.getenv("ARTIFACTS_DIR", "artifacts")),
        realtime_model=os.getenv("OPENAI_REALTIME_MODEL", "gpt-realtime-2"),
        realtime_voice=os.getenv("OPENAI_REALTIME_VOICE", "marin"),
        realtime_female_voice=os.getenv("OPENAI_REALTIME_FEMALE_VOICE", "marin"),
        realtime_male_voice=os.getenv("OPENAI_REALTIME_MALE_VOICE", "cedar"),
        realtime_session_style=os.getenv("OPENAI_REALTIME_SESSION_STYLE", "ga"),
        analysis_model=os.getenv("OPENAI_ANALYSIS_MODEL", "gpt-5.5"),
        transcription_model=os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-transcribe"),
        initial_greeting_delay_ms=int(os.getenv("INITIAL_GREETING_DELAY_MS", "1200")),
        initial_audio_ignore_ms=int(os.getenv("INITIAL_AUDIO_IGNORE_MS", "8000")),
        vad_threshold=float(os.getenv("VAD_THRESHOLD", "0.45")),
        vad_prefix_padding_ms=int(os.getenv("VAD_PREFIX_PADDING_MS", "350")),
        vad_silence_duration_ms=int(os.getenv("VAD_SILENCE_DURATION_MS", "850")),
        run_suite_spacing_seconds=int(os.getenv("RUN_SUITE_SPACING_SECONDS", "45")),
        max_call_seconds=int(os.getenv("MAX_CALL_SECONDS", "180")),
    )


def normalize_e164(number: str) -> str:
    raw = number or ""
    cleaned = re.sub(r"[^\d+]", "", raw)
    if not cleaned:
        if raw.strip():
            raise ConfigError(f"Phone number is not valid E.164: {number!r}")
        return ""
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    if not cleaned.startswith("+") and len(cleaned) == 11 and cleaned.startswith("1"):
        cleaned = "+" + cleaned
    if not cleaned.startswith("+") and len(cleaned) == 10:
        cleaned = "+1" + cleaned
    if not re.fullmatch(r"\+[1-9]\d{7,14}", cleaned):
        raise ConfigError(f"Phone number is not valid E.164: {number!r}")
    return cleaned


def resolve_env_file(env_file: str | Path) -> Path:
    path = Path(env_file)
    if path.is_absolute() or path.exists() or path.name != ".env":
        return path
    project_env = Path(__file__).resolve().parents[2] / ".env"
    if project_env.exists():
        return project_env
    return path


def assert_assessment_target(number: str, settings: Settings) -> str:
    normalized = normalize_e164(number)
    expected = normalize_e164(settings.target_test_number)
    if normalized != expected or expected != TARGET_TEST_NUMBER:
        raise TargetNumberError(
            f"Refusing to call {normalized}. This bot is hard-locked to {TARGET_TEST_NUMBER}."
        )
    return normalized


def require_live_call_settings(settings: Settings) -> None:
    missing = [
        name
        for name, value in {
            "OPENAI_API_KEY": settings.openai_api_key,
            "TWILIO_ACCOUNT_SID": settings.twilio_account_sid,
            "TWILIO_AUTH_TOKEN": settings.twilio_auth_token,
            "TWILIO_FROM_NUMBER": settings.twilio_from_number,
            "PUBLIC_BASE_URL": settings.public_base_url,
        }.items()
        if not value
    ]
    if missing:
        raise ConfigError(f"Missing required environment variables: {', '.join(missing)}")
    assert_assessment_target(settings.target_test_number, settings)


def public_http_to_ws(public_base_url: str, path: str) -> str:
    base = public_base_url.rstrip("/")
    parsed = urlparse(base if "://" in base else f"https://{base}")
    scheme = "wss" if parsed.scheme == "https" else "ws"
    host = parsed.netloc or parsed.path
    prefix_path = "" if parsed.netloc else ""
    if parsed.netloc and parsed.path:
        prefix_path = parsed.path.rstrip("/")
    return f"{scheme}://{host}{prefix_path}{path}"
