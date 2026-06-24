# Call Evidence Summary

The assignment evaluates voice interaction quality before code review. I selected the final calls based on conversation completeness, audio duration, long pauses, transcript consistency, scenario coverage, and bug evidence quality.

## What Was Checked

- Every primary selected call has an MP3 recording in `submission/recordings/` and a matching transcript in `submission/transcripts/`.
- The primary selected set includes 12 calls, which is above the 10-call minimum.
- Calls target only `+18054398008` and use the single caller number documented in `SUBMISSION.md`.
- Reruns were added after reviewing the first call set for steering and patient-language issues.
- `ffprobe` duration checks confirm the selected calls are generally full conversations.
- `ffmpeg` silence detection found only two pauses just over 4 seconds: `d8280b05d6` and `691aba52fd`.

## Audio Duration Summary

| Call | Scenario | Duration |
| --- | --- | ---: |
| `10ca193260` | Simple appointment rerun | 147.9s |
| `2d3be69cb3` | Office logistics rerun | 95.8s |
| `64e1556ea2` | Reschedule existing rerun | 154.2s |
| `691aba52fd` | Insurance question rerun | 89.6s |
| `c62b8aa717` | Medication refill rerun | 101.1s |
| `d8280b05d6` | Simple appointment DOB mismatch issue | 159.1s |
| `suite-03-35700e` | Weekend hours | 152.5s |
| `suite-07-a48052` | Urgent boundary | 149.8s |
| `suite-08-ad7ed0` | Spelling correction | 132.9s |
| `suite-09-f85ec3` | Barge-in | 98.0s |
| `suite-10-fd7cf1` | Ambiguous request | 161.0s |
| `suite-11-1cd272` | Human handoff | 53.5s |

## Strongest Calls

These calls have the clearest combination of natural flow, complete evidence, and meaningful signal:

- `2d3be69cb3`: clean logistics question flow; shows the bot can ask realistic front-desk questions without getting stuck in verification.
- `691aba52fd`: clean insurance question flow; agent answers with an appropriate coverage caveat.
- `64e1556ea2`: stronger rescheduling test; caller actively steers back to the goal and exposes the verification/handoff failure.
- `suite-07-a48052`: strong safety signal; chest-tightness guidance delayed.
- `suite-11-1cd272`: short but very clear failed human handoff.
- `c62b8aa717`: useful refill workflow failure before actionable refill details are collected.
- `suite-10-fd7cf1`: good ambiguous-request clarification followed by scheduling/handoff failure.

## Watch Items

These calls are useful but have context worth noting:

- `d8280b05d6`: retained because it exposes a strong DOB mismatch issue; the caller has one clinic-like phrase and a short post-goodbye correction.
- `c62b8aa717`: useful refill evidence, but the caller has one slightly clinic-like phrase.
- `suite-09-f85ec3`: included for changed-preference/barge-in coverage, but it is weaker than the other scenario calls because overlap was limited.
- `suite-11-1cd272`: shorter than the usual 1-3 minute range, but complete for a handoff-failure scenario.

## Recommendation

The primary evidence set is the 12 calls in `submission/recordings/` and `submission/transcripts/`.
