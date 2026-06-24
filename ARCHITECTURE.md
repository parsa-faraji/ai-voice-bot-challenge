# Architecture

The main design choice was to optimize for the part of the challenge that gets judged first: whether the caller sounds like a real patient.

A bot that places calls but feels scripted would not be useful for this assessment. I used Twilio for outbound calling and recording, and OpenAI Realtime for the live patient voice.

## Call Flow

`Twilio outbound call -> TwiML <Connect><Stream> -> FastAPI /media -> OpenAI Realtime -> Twilio media stream`

Twilio places the outbound call and records both sides.

The FastAPI server returns TwiML with `<Connect><Stream>`, then handles the live media WebSocket at `/media`. The bridge forwards Twilio's G.711 audio chunks to OpenAI Realtime and streams generated patient audio back to Twilio.

The bridge intentionally ignores the first few seconds of inbound audio before forwarding it to Realtime. The assessment line starts with an automated recording disclosure and Spanish-language option; early pilots showed that a realtime caller can accidentally treat that disclosure as the agent's first turn. `INITIAL_AUDIO_IGNORE_MS` prevents the patient from answering the disclosure while still allowing the model to hear the real greeting.

## Stack Choices

- **Python + uv**: simple packaging, repeatable setup, and a single `voicebot` CLI entry point.
- **Typer + Rich**: readable command-line workflows for `doctor`, `call`, `run-suite`, `fetch-artifacts`, `evaluate-transcripts`, and `analyze`.
- **FastAPI + uvicorn**: a small web server for TwiML, health checks, stream-status callbacks, and the media WebSocket.
- **Twilio Programmable Voice**: real outbound phone calls, dual-channel MP3 recordings, and bidirectional media streaming.
- **OpenAI Realtime**: live patient speech with lower latency and more natural prosody than a separate STT -> LLM -> TTS pipeline.

Realtime was a tradeoff.

A traditional pipeline would give more control over exact wording. It would also add latency and make turn-taking harder.

Realtime gives better pacing, so I accepted less deterministic wording and added stricter scenario prompts, transcript linting, and audio review.

Because Twilio places real outbound calls, the code is hard-locked to `+18054398008`.

## Caller Design

The caller is hybrid scripted plus adaptive.

Each scenario defines the patient identity, voice profile, first-turn identity response, facts, stressors, and success criteria. The model chooses the actual wording during the call.

That keeps the patient flexible enough to answer naturally while still steering toward scheduling, refills, triage, handoff, and edge cases.

The scenario layer also defines phone-number behavior. Routine record-specific workflows provide the configured caller number when asked. The forgotten-phone scenario is the only one that intentionally cannot provide the phone number on file.

## Evidence Discipline

MP3 recordings are the source of truth.

Realtime transcript events are useful for quick debugging, but a transcript is not treated as proof by itself. Submitted transcripts are promoted only after comparing them against the MP3 recording.

`evaluate-transcripts` screens for patient-bot issues before a call is promoted, including accidental phone-number failures outside the one scenario designed to test that edge.

The analyzer can draft findings, but the submitted bug report only includes audio-defensible product issues.
