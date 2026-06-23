# Athena Voice Bot Challenge

Python voice bot for the Pretty Good AI AI Engineering Challenge. It calls only the assessment line, behaves like a realistic patient, records/transcribes conversations, and produces a first-pass bug report.

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

If `ngrok` is not installed, this machine already has `cloudflared`:

```bash
cloudflared tunnel --url http://localhost:8000
```

Set `PUBLIC_BASE_URL` in `.env` to the HTTPS tunnel URL, then verify:

```bash
uv run voicebot doctor
uv run voicebot twiml appointment-simple
```

## Run Calls

Run CLI commands from the repository root:

```bash
cd /Users/parsafarajialamouti/ai-voice-bot-challenge
```

If you are in another directory, use:

```bash
uv run --project /Users/parsafarajialamouti/ai-voice-bot-challenge voicebot doctor
```

Dry-run the suite first:

```bash
uv run voicebot run-suite --count 12 --dry-run
```

Place one pilot call, listen to it, tune if needed, then run the full suite:

```bash
uv run voicebot call appointment-simple --yes
uv run voicebot run-suite --count 12 --yes
```

To continue after a pilot call and avoid duplicating the first scenario:

```bash
uv run voicebot run-suite --start-index 2 --count 11 --spacing-seconds 10 --yes
```

After calls complete:

```bash
uv run voicebot fetch-artifacts
uv run voicebot analyze
```

Artifacts are written under `artifacts/`:

- `recordings/*.mp3`: Twilio call recordings
- `transcripts/*.txt`: speaker-labeled transcripts reconstructed from Realtime transcript events
- `BUG_REPORT.md`: first-pass bug report for manual review

Calls default to a 180-second Twilio time limit (`MAX_CALL_SECONDS`) so a pilot or suite call cannot run open-ended. `run-suite` waits for each call to complete before starting the next one; overlapping calls usually sound worse and make artifacts harder to review.

## Submission Checklist

- Minimum 10 complete 1-3 minute calls. This repo includes 12 selected calls in `submission/`.
- MP3 recording for every submitted call
- Transcript for every submitted call
- `ARCHITECTURE.md`
- `SCENARIOS.md`
- `BUG_REPORT.md` and `submission/BUG_REPORT.md`
- `CALL_QA.md` and `CALL_EVALUATION.md`
- `SUBMISSION.md`
- Loom walkthrough link in this README before submission
- 5-minute screen recording showing AI-assisted debugging/fixing

## Loom Links

- Walkthrough: TODO
- AI debugging/fix recording: TODO
