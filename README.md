# Athena Voice Bot Challenge

Python voice bot for the Pretty Good AI AI Engineering Challenge. It calls only the assessment line, behaves like a realistic patient, records/transcribes conversations, and produces a curated bug report grounded in call evidence.

## Safety

The code is hard-locked to `+1-805-439-8008` (`+18054398008`). `voicebot call` and `voicebot run-suite` do not place live calls unless `--yes` is passed.

## Setup

```bash
uv sync
cp .env.example .env
```

Fill in `.env` with OpenAI and Twilio credentials. `TWILIO_FROM_NUMBER` must be the one number used for every assessment call.

Expose the local server with ngrok, cloudflared, or another HTTPS tunnel:

```bash
uv run voicebot serve --port 8000
ngrok http 8000
```

If `ngrok` is not installed, `cloudflared` works as an alternative:

```bash
cloudflared tunnel --url http://localhost:8000
```

Set `PUBLIC_BASE_URL` in `.env` to the HTTPS tunnel URL, then verify:

```bash
uv run voicebot doctor --strict
uv run voicebot twiml appointment-simple
```

## Run Calls

Run CLI commands from the repository root.

Dry-run the suite first:

```bash
uv run voicebot run-suite --count 14 --dry-run
```

Place one pilot call, listen to it, tune if needed, then run the full suite:

```bash
uv run voicebot call appointment-simple --yes
uv run voicebot run-suite --count 14 --yes
```

To continue after a pilot call and avoid duplicating the first scenario:

```bash
uv run voicebot run-suite --start-index 2 --count 13 --spacing-seconds 10 --yes
```

To inspect the committed submission transcripts:

```bash
uv run voicebot evaluate-transcripts submission/transcripts
```

After running new calls locally:

```bash
uv run voicebot fetch-artifacts
uv run voicebot evaluate-transcripts artifacts/transcripts
uv run voicebot analyze
```

The committed submission evidence lives in:

- `submission/recordings/*.mp3`: selected Twilio call recordings
- `submission/transcripts/*.txt`: selected speaker-labeled transcripts
- `submission/BUG_REPORT.md`: curated findings for review

When running new calls locally, generated runtime output is written under the gitignored `artifacts/` directory:

- `recordings/*.mp3`: Twilio call recordings
- `transcripts/*.txt`: speaker-labeled transcripts reconstructed from Realtime transcript events
- `BUG_REPORT.md`: generated draft bug report for local review

Use `evaluate-transcripts` before promoting new local calls into `submission/`. It screens for patient-bot issues such as missed identity answers, unnatural filler, staff-like phrasing, delayed DOB/spelling answers, overlong turns, and substantive comments after the agent has ended the call.

Calls default to a 180-second Twilio time limit (`MAX_CALL_SECONDS`) so a pilot or suite call cannot run open-ended. `run-suite` waits for each call to complete before starting the next one; overlapping calls usually sound worse and make artifacts harder to review.

## Voice Tuning

Twilio carries the bidirectional phone audio, but the caller's voice and turn-taking come from the Realtime session. Each scenario has a male or female voice profile, selected through `OPENAI_REALTIME_MALE_VOICE` and `OPENAI_REALTIME_FEMALE_VOICE`; `OPENAI_REALTIME_VOICE` is only the fallback. Use `VAD_SILENCE_DURATION_MS` to tune pacing; higher values make the patient wait longer after the practice agent stops speaking, while lower values make the patient respond faster.
