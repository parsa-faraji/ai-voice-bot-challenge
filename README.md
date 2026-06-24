# Athena Voice Bot Challenge

Python voice bot for the Pretty Good AI AI Engineering Challenge.

The bot calls the assessment line as a realistic patient. It records both sides, rebuilds speaker-labeled transcripts, and supports a bug report grounded in the recordings.

The reviewed submission evidence is in `submission/`.

## Included

- Working Python voice bot
- 12 selected MP3 recordings
- 12 matching speaker-labeled transcripts
- Curated bug report
- 14 configured patient scenarios
- Transcript and caller-quality checks

## Safety

The caller is hard-locked to the assessment number:

`+1-805-439-8008` (`+18054398008`)

`voicebot call` and `voicebot run-suite` will not place live calls unless `--yes` is passed.

## Setup

```bash
uv sync
cp .env.example .env
```

Fill in `.env` with OpenAI and Twilio credentials.

`TWILIO_FROM_NUMBER` must be the one phone number used for every assessment call.

Start the local server:

```bash
uv run voicebot serve --port 8000
```

Expose it with an HTTPS tunnel:

```bash
ngrok http 8000
```

If `ngrok` is not installed, `cloudflared` also works:

```bash
cloudflared tunnel --url http://localhost:8000
```

Set `PUBLIC_BASE_URL` in `.env` to the HTTPS tunnel URL.

Check the setup before calling:

```bash
uv run voicebot doctor --strict
uv run voicebot twiml appointment-simple
```

## Run Calls

Dry-run the suite:

```bash
uv run voicebot run-suite --count 14 --dry-run
```

Place one pilot call:

```bash
uv run voicebot call appointment-simple --yes
```

Listen to that call before running the suite.

Run all built-in scenarios:

```bash
uv run voicebot run-suite --count 14 --yes
```

To continue after a pilot call and avoid repeating the first scenario:

```bash
uv run voicebot run-suite --start-index 2 --count 13 --spacing-seconds 10 --yes
```

## Evidence Workflow

Inspect the committed submission transcripts:

```bash
uv run voicebot evaluate-transcripts submission/transcripts
```

After running new calls locally:

```bash
uv run voicebot fetch-artifacts
uv run voicebot evaluate-transcripts artifacts/transcripts
uv run voicebot analyze
```

`artifacts/` is local runtime output. It is intentionally gitignored. The public evidence set lives in `submission/`.

Committed submission evidence:

- `submission/recordings/*.mp3`
- `submission/transcripts/*.txt`
- `submission/BUG_REPORT.md`

Local artifacts created after new calls:

- `artifacts/recordings/*.mp3`
- `artifacts/transcripts/*.txt`
- `artifacts/BUG_REPORT.md`

Use `evaluate-transcripts` before promoting new calls into `submission/`. It screens for caller-side problems such as missed identity answers, staff-like phrasing, overlong turns, repeated filler, and substantive comments after the agent has ended the call.

Calls default to a 180-second Twilio time limit through `MAX_CALL_SECONDS`. `run-suite` waits for each call to complete before starting the next one.

## Voice Tuning

Twilio carries the phone audio. OpenAI Realtime controls the patient voice and turn-taking.

Each scenario can use a male or female voice profile:

- `OPENAI_REALTIME_MALE_VOICE`
- `OPENAI_REALTIME_FEMALE_VOICE`
- `OPENAI_REALTIME_VOICE` as fallback

Use `VAD_SILENCE_DURATION_MS` to tune pacing. Higher values make the patient wait longer after the practice agent stops speaking. Lower values make the patient respond faster.

## Repo Map

- `src/voicebot/`: caller, bridge, Twilio client, Realtime session, evaluator, analyzer
- `tests/`: unit tests for config, TwiML, scenarios, prompts, diagnostics, transcripts, and evaluator behavior
- `submission/`: selected recordings, transcripts, and submitted bug report
- `ARCHITECTURE.md`: design choices and tradeoffs
- `SCENARIOS.md`: scenario coverage
- `CALL_SELECTION.md`: how calls were chosen
- `CALL_EVIDENCE.md`: evidence checks and duration summary
- `ITERATION_LOG.md`: what changed after reviewing real calls
