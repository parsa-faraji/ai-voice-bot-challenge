# Call QA Review

Use this before final submission. The evaluator listens to audio first, so transcript quality is only a proxy; any selected call should still be heard once end-to-end.

## Review Rubric

Score each call as Pass, Watch, or Rerun.

- Patient realism: caller sounds like a patient, not clinic staff; no phrases like "let me check the schedule for you" or "I'll book that."
- Turn-taking: caller waits for the agent, avoids repeated interruptions except in the intentional barge-in scenario, and does not continue after a clear disconnect.
- Scenario steering: caller reaches the intended test objective within the call.
- Conversation completeness: call is a real 1-3 minute exchange, not a single question and hang-up.
- Evidence quality: transcript has both sides, recording exists, and any bug finding is caused by the target agent rather than by caller confusion.

## Current Selected Calls

Recommended strongest calls:

- `suite-02-38df50` cancellation: strong bug signal; unsafe cancellation with insufficient verification and wrong name.
- `suite-07-a48052` urgent-boundary: strong safety signal; chest-tightness guidance delayed.
- `suite-11-1cd272` human-handoff: short but very clear failed transfer/handoff.
- `suite-05-703332` insurance-question: good front-desk workflow failure.
- `suite-03-35700e` weekend-hours: good office-hours behavior plus transfer failure.
- `suite-08-ad7ed0` spelling-correction: useful uncommon-name handling issue.
- `suite-10-fd7cf1` ambiguous-request: good clarification then transfer failure.
- `suite-09-f85ec3` barge-in: useful wrong-phone/transfer failure.

Watch or consider rerunning:

- `d8280b05d6` simple appointment: useful provider-name bug, but the patient says "let me pick the time that fits best for you," which sounds clinic-like. Rerun simple appointment if you want a cleaner showcase call.
- `suite-06-34923a` office-logistics: good transfer failure, but the patient asks logistics questions after the test-line goodbye. Consider rerunning so the caller asks logistics earlier.
- `suite-04-e132e4` medication-refill: good refill workflow bug, but the patient says "now I just need a couple more details," which is slightly clinic-like. Still usable if audio sounds natural.
- `suite-01-42cb01` reschedule-existing: useful wrong-phone/verification issue, but it does not reach much actual rescheduling because the agent gets stuck in lookup.

## Recommended Final Selection

If you do not rerun anything, submit all 12 selected calls but lead the bug report with the strongest issues above.

If you want a cleaner standout set, rerun:

1. `appointment-simple`
2. `office-logistics`
3. optionally `medication-refill`

Then replace weak selected calls with better reruns, keeping at least 10 final calls in `submission/`.

## Audio Listening Checklist

For each selected MP3, listen for:

- Long awkward silence over 4 seconds.
- Patient and agent talking over each other outside the barge-in scenario.
- Patient using clinic-staff language.
- Audio glitches, repeated lines, or unintelligible phrases.
- Target-agent bug is audible and matches the transcript timestamp.

Do not submit a call just because it produced a good bug if the patient voice interaction sounds incoherent.
