# Submission Manifest

## Caller Number

All live assessment calls were placed from:

`+18339589786`

All calls targeted only:

`+18054398008`

## Primary Selected Calls

Use the 13 calls in `submission/recordings/` and `submission/transcripts/` for final review. They cover scheduling, rescheduling, cancellation, medication refill, insurance, office logistics, urgent triage, spelling correction, interruption, ambiguity, and human handoff.

Primary selected runs:

- `10ca193260` - appointment-simple rerun
- `2d3be69cb3` - office-logistics rerun
- `64e1556ea2` - reschedule-existing rerun
- `691aba52fd` - insurance-question rerun
- `c62b8aa717` - medication-refill rerun
- `d8280b05d6` - appointment-simple DOB/provider issue
- `suite-02-38df50` - cancel appointment
- `suite-03-35700e` - weekend hours
- `suite-07-a48052` - urgent boundary
- `suite-08-ad7ed0` - spelling correction
- `suite-09-f85ec3` - barge-in/changed preference
- `suite-10-fd7cf1` - ambiguous request
- `suite-11-1cd272` - human handoff

## Iteration Evidence

Superseded earlier calls live under `submission/superseded/`. They are retained to show before/after review and iteration, but they are not the primary review set.

The first rough pilot call is retained under ignored local `artifacts/` only and should not be treated as a selected submission call.

## Selected Artifacts

- `submission/recordings/*.mp3`
- `submission/transcripts/*.txt`
- `submission/BUG_REPORT.md`
- `BUG_REPORT.md`
- `CALL_SELECTION.md`
- `CALL_EVIDENCE.md`
- `ITERATION_LOG.md`
- `ARCHITECTURE.md`
- `SCENARIOS.md`
- `README.md`
