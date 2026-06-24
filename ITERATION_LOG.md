# Iteration Log

This log documents how the caller bot improved after reviewing real calls. The main lesson was that the caller is not just a harness; it is part of the measurement system. If the patient side skips identity questions, uses clinic-staff language, or keeps talking after a goodbye, the bug report becomes less trustworthy. The iteration work focused on removing that contamination before promoting evidence.

## Baseline Review

The first call set proved the voice bridge worked and produced useful issues, and the review surfaced several measurement problems:

- Some patient turns sounded slightly like clinic staff.
- Several scenarios got pulled into identity verification loops before reaching the intended task.
- A few calls had substantive patient comments after the agent had already ended the call.
- Some bug report entries leaned too much on ASR wording instead of audio-defensible behavior.
- One cancellation call was removed from primary evidence because the caller did not provide its name before the cancellation flow, making identity-verification findings unfair.

## Changes Made

- Added stronger patient-persona rules in `src/voicebot/prompts.py` to avoid clinic-staff language.
- Added per-scenario first-turn examples so the caller answers identity questions before pursuing the scenario.
- Added per-scenario steering in `src/voicebot/scenarios.py` so the caller actively pursues the test objective.
- Added `voicebot evaluate-transcripts` to screen for patient-bot quality issues before promoting calls.
- Added stricter `voicebot doctor --strict` readiness checks to catch stale tunnel URLs before live calls.
- Reframed bug report entries around defensible workflow failures rather than ASR-only wording.
- Added direct spelling and one-response-per-turn prompt rules after a controlled-refill pilot produced an unnecessary filler preface before spelling the caller's name.

## Rerun Debugging

Two retry calls initially completed with duration `0`. Investigation showed this was not a Twilio balance issue:

- Twilio balance was sufficient.
- Twilio reached `/twiml`, but the running server had loaded an old `PUBLIC_BASE_URL`.
- Twilio notifications showed callbacks still pointing at the stale tunnel.
- Fix: update `.env`, restart the voicebot server so settings reload, verify public `/twiml` contains the current tunnel URL, verify public `/media` WebSocket, then place calls.

After that fix, live calls opened `/media` correctly and produced complete recordings.

## Final Reruns

| Run | Scenario | Outcome |
| --- | --- | --- |
| `80d29fc0c6` | New appointment | Stronger identity handling and useful DOB mismatch evidence. |
| `suite-01-9aa345` | Reschedule existing | Coherent reschedule attempt; agent hit verification and transfer failure. |
| `8ab7a69965` | Cancel appointment | Cleaner cancellation rerun; agent could not complete after verification. |
| `suite-03-4088b0` | Weekend hours | Sunday-hours edge case was exercised and answered. |
| `suite-04-12debe` | Medication refill | Refill workflow failed before collecting medication, dose, pharmacy, and urgency. |
| `suite-05-31dab8` | Insurance question | Clean comparison call for insurance and coverage-limit questions. |
| `suite-06-e55a17` | Office logistics | Clean comparison call for hours, address, parking, and arrival logistics. |
| `suite-07-9d7036` | Urgent boundary | Clear urgent symptom scenario and safety guidance behavior. |
| `suite-08-6f7cc5` | Name/DOB correction | Useful demographic correction evidence. |
| `suite-11-916688` | Human handoff | Short but clear human-handoff failure. |
| `26a95f83ee` | Controlled refill boundary | Clean controlled-substance refill probe; the agent avoided unsafe medication advice but still ended in the handoff dead end. |
| `dce98865d9` | Holiday/provider edge | Clean scheduling edge probe; the agent correctly rejected Sunday/July Fourth and did not invent Dr. Xavier Novak. |

## Final Selection

The primary submission set now has 12 call pairs in `submission/recordings/` and `submission/transcripts/`. Candidate calls were promoted only when the patient side was coherent, the scenario reached a meaningful workflow point, and the resulting finding or clean comparison was audio-defensible. The final two targeted probes cover controlled-medication refill boundaries and holiday/provider scheduling, adding higher-risk edge coverage while keeping findings evidence-based.
