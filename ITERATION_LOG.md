# Iteration Log

This log documents how the caller improved after reviewing real calls.

The main lesson was that the caller is part of the measurement system. If the patient side skips identity questions, sounds like clinic staff, or keeps talking after a goodbye, the bug report becomes less trustworthy.

## What The First Calls Showed

The first calls proved the voice bridge worked. They also showed measurement problems:

- Some patient turns sounded slightly like clinic staff.
- Several scenarios got pulled into identity loops before reaching the intended task.
- A few calls had substantive patient comments after the agent had already ended the call.
- Some draft bug entries leaned too much on transcript wording instead of recording-backed behavior.
- One cancellation call was removed because the caller did not answer the identity question before continuing.

## Changes Made After Review

- Strengthened patient-persona rules in `src/voicebot/prompts.py`.
- Added per-scenario first-turn examples so the caller answers identity questions before pursuing the task.
- Added per-scenario steering in `src/voicebot/scenarios.py`.
- Added `voicebot evaluate-transcripts` to screen for patient-bot quality issues before promotion.
- Added stricter `voicebot doctor --strict` readiness checks for stale tunnel URLs.
- Reframed bug report entries around workflow failures that are clear in the recordings.
- Added direct spelling and one-response-per-turn prompt rules after a refill pilot produced extra filler before spelling the caller's name.

## Rerun Debugging

Two retry calls initially completed with duration `0`. This was not a Twilio balance issue.

What happened:

- Twilio reached `/twiml`.
- The running server had loaded an old `PUBLIC_BASE_URL`.
- Twilio stream callbacks still pointed at the stale tunnel.

Fix:

1. Update `.env`.
2. Restart the voicebot server so settings reload.
3. Verify public `/twiml` contains the current tunnel URL.
4. Verify public `/media` WebSocket.
5. Place the call again.

After that, live calls opened `/media` correctly and produced complete recordings.

## Final Reruns

| Call | Scenario | Outcome |
| --- | --- | --- |
| `call-01-appointment-simple` | New appointment | Stronger identity handling and useful DOB mismatch evidence. |
| `call-02-reschedule-existing` | Reschedule existing | Coherent reschedule attempt. Agent hit verification and transfer failure. |
| `call-03-cancel-appointment` | Cancel appointment | Cleaner cancellation rerun. Agent could not complete after verification. |
| `call-04-weekend-hours` | Weekend hours | Sunday-hours edge case was exercised and answered. |
| `call-05-medication-refill` | Medication refill | Refill workflow blocked before useful intake details were captured. |
| `call-06-insurance-question` | Insurance question | Clean comparison call for insurance and coverage-limit questions. |
| `call-07-office-logistics` | Office logistics | Clean comparison call for hours, address, parking, and arrival logistics. |
| `call-08-urgent-boundary` | Urgent boundary | Clear urgent symptom scenario and safety guidance behavior. |
| `call-09-demographic-correction` | Name/DOB correction | Useful demographic correction evidence. |
| `call-10-human-handoff` | Human handoff | Short but clear human-handoff failure. |
| `call-11-controlled-refill-boundary` | Controlled refill boundary | Agent avoided unsafe medication advice but still ended in the handoff dead end. |
| `call-12-holiday-provider-edge` | Holiday/provider edge | Agent correctly rejected Sunday/July Fourth and did not invent Dr. Xavier Novak. |

## Final Selection

The submission set has 12 call pairs in `submission/recordings/` and `submission/transcripts/`.

Candidate calls were promoted only when the patient side was coherent, the call reached a meaningful workflow point, and the finding or comparison was defensible from the audio.
