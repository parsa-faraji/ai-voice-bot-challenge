from pathlib import Path

import pytest

from voicebot.artifacts import ArtifactStore
from voicebot.bridge import BridgeState, MediaBridge
from voicebot.config import TARGET_TEST_NUMBER, Settings


def settings(tmp_path: Path) -> Settings:
    return Settings(
        openai_api_key="sk-test",
        twilio_account_sid="AC123",
        twilio_auth_token="token",
        twilio_from_number="+13334445555",
        target_test_number=TARGET_TEST_NUMBER,
        public_base_url="https://example.ngrok.app",
        artifacts_dir=tmp_path,
        initial_audio_ignore_ms=8000,
    )


def test_initial_audio_gate_skips_disclosure_window(tmp_path, monkeypatch):
    bridge = MediaBridge(settings(tmp_path), ArtifactStore(tmp_path))
    state = BridgeState()

    monkeypatch.setattr(state, "elapsed", lambda: 7.5)

    assert bridge._should_forward_remote_audio(state) is False


def test_initial_audio_gate_opens_after_disclosure_window(tmp_path, monkeypatch):
    bridge = MediaBridge(settings(tmp_path), ArtifactStore(tmp_path))
    state = BridgeState()

    monkeypatch.setattr(state, "elapsed", lambda: 8.1)

    assert bridge._should_forward_remote_audio(state) is True


def test_initial_response_fallback_waits_for_audio_gate(tmp_path):
    bridge = MediaBridge(settings(tmp_path), ArtifactStore(tmp_path))

    assert bridge._initial_response_delay_ms() == 9200
