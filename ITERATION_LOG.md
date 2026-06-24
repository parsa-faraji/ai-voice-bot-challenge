# Iteration Log

This log documents how the caller bot improved after reviewing real calls. It is organized around the assignment rubric: lucid voice interaction first, useful bug evidence second, then working code and clear thinking.

## Baseline Review

The first selected call set was coherent and produced useful bugs, but several calls had quality risks:

- Some patient turns sounded slightly like clinic staff, for example asking what worked best "for you."
- Several scenarios got pulled into identity verification loops before reaching the intended task.
- A few calls had substantive patient comments after the agent had already ended the call.
- Some bug report entries leaned too much on ASR wording instead of audio-defensible behavior.
- One cancellation call was later removed from the primary set because the caller did not provide its name before the cancellation flow, making an identity-verification finding unfair.

## Changes Made

- Added stronger patient-persona rules in `src/voicebot/prompts.py` to avoid clinic-staff language.
- Added per-scenario steering in `src/voicebot/scenarios.py` so the caller actively pursues the test objective.
- Added stricter natural-conversation rules so the caller answers direct identity questions first and includes its name if the agent asks for DOB before identity is established.
- Reframed bug report entries around defensible workflow failures rather than ASR-only wording.
- Added `CALL_SELECTION.md` and `CALL_EVIDENCE.md` to make the final call-selection rationale explicit.

## Rerun Debugging

Two retry calls initially completed with duration `0`. Investigation showed this was not a Twilio balance issue:

- Twilio balance was about `$19.298`.
- Twilio reached `/twiml`, but the running server had loaded an old `PUBLIC_BASE_URL`.
- Twilio notifications showed callbacks still pointing at the stale tunnel.
- Fix: update `.env`, restart the voicebot server so settings reload, verify public `/twiml` contains the current tunnel URL, verify public `/media` WebSocket, then place calls.

After that fix, live calls opened `/media` correctly and produced complete recordings.

## Targeted Reruns

| Run | Scenario | Duration | Outcome |
| --- | --- | ---: | --- |
| `10ca193260` | Simple appointment | 147.9s | Completed scheduling; cleaner than the earlier appointment call but kept alongside it because the earlier call exposed DOB mismatch behavior. |
| `2d3be69cb3` | Office logistics | 95.8s | Strong improvement: caller asked hours, address, parking, and arrival timing before verification; agent answered directly. |
| `691aba52fd` | Insurance question | 89.6s | Strong improvement: caller asked Aetna PPO question directly; agent answered and gave coverage caveat. |
| `64e1556ea2` | Reschedule existing | 154.2s | Stronger evidence: caller repeatedly steered to rescheduling; agent still failed in verification/handoff path. |
| `c62b8aa717` | Medication refill | 101.1s | Useful evidence: caller asked for refill and tried to provide missing details; agent transferred before collecting actionable refill information. |

## Final Selection

The primary submission set now has 12 call pairs in `submission/recordings/` and `submission/transcripts/`. Weaker earlier calls were moved to `submission/superseded/` so the repo preserves iteration evidence without making those calls the primary review set.

The submission highlights this arc:

1. The first calls proved the bridge worked and uncovered real issues.
2. Manual and independent review found caller-quality risks.
3. Prompt/scenario changes targeted those risks.
4. Reruns showed better steering and cleaner patient behavior.
5. The final bug report was tightened to focus on audio-defensible issues.
