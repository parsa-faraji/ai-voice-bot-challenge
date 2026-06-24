# Call Selection Rationale

The final selection prioritizes coherent voice interaction first, then bug usefulness and scenario coverage. Transcript quality is treated as a proxy; the MP3 recordings are the source of truth.

## Review Rubric

Score each call as Pass, Watch, or Exclude.

- Patient realism: caller sounds like a patient, not clinic staff.
- Turn-taking: caller waits for the agent, avoids repeated interruptions except in the intentional barge-in scenario, and does not continue with new content after a clear disconnect.
- Scenario steering: caller reaches or actively pursues the intended test objective.
- Conversation completeness: call is a real exchange, not a single question and hang-up.
- Evidence quality: transcript has both sides, recording exists, and bug findings are caused by the target agent rather than caller confusion.

## Final Primary Set

Pass:

- `2d3be69cb3` office-logistics rerun: strong patient realism and direct task completion.
- `691aba52fd` insurance-question rerun: strong patient realism and direct answer with coverage caveat.
- `64e1556ea2` reschedule-existing rerun: caller actively steers; agent fails verification/handoff.
- `suite-07-a48052` urgent-boundary: strong safety signal.
- `suite-10-fd7cf1` ambiguous-request: good clarification then workflow failure.
- `suite-03-35700e` weekend-hours: useful hours/scheduling behavior.

Watch but keep:

- `10ca193260` appointment-simple rerun: completed scheduling and cleaner than the earlier appointment call, with one slightly awkward patient line.
- `d8280b05d6` appointment-simple: retained for the DOB mismatch bug despite one clinic-like phrase.
- `c62b8aa717` medication-refill rerun: useful refill failure, with one clinic-like phrase.
- `suite-08-ad7ed0` spelling-correction: useful demographic correction failure.
- `suite-09-f85ec3` barge-in: weaker overlap evidence, but covers changed preference/interruption.
- `suite-11-1cd272` human-handoff: short but complete failed handoff.

## Audio Checks

- Primary selected recordings: 12
- Primary selected transcripts: 12
- Detected pauses over 4 seconds: `d8280b05d6` and `691aba52fd`, both about 4.2 seconds.
- No primary selected call lacks a matching transcript.

The current primary set balances useful bug evidence with clearer voice interaction.
