# Call Evaluation Notes

This review is a quality gate before final submission. The assignment says voice interaction quality is evaluated before code review, so the selected calls were checked for conversation completeness, audio duration, long pauses, transcript consistency, scenario coverage, and bug evidence quality.

## What Was Checked

- Every selected call has an MP3 recording in `submission/recordings/` and a matching transcript in `submission/transcripts/`.
- The selected set includes 12 calls, which is above the 10-call minimum.
- Calls target only `+18054398008` and use the single caller number documented in `SUBMISSION.md`.
- Independent MP3 transcription was run as a sanity check against the saved transcripts.
- `ffprobe` duration checks confirm the selected calls are generally full conversations.
- `ffmpeg` silence detection found no major silence issue except one 4.2-second pause in the simple appointment pilot.

## Audio Duration Summary

| Call | Scenario | Duration |
| --- | --- | ---: |
| `d8280b05d6` | Simple appointment | 159.1s |
| `suite-01-42cb01` | Reschedule existing | 157.7s |
| `suite-02-38df50` | Cancel appointment | 83.0s |
| `suite-03-35700e` | Weekend hours | 152.5s |
| `suite-04-e132e4` | Medication refill | 107.3s |
| `suite-05-703332` | Insurance question | 120.1s |
| `suite-06-34923a` | Office logistics | 133.7s |
| `suite-07-a48052` | Urgent boundary | 149.8s |
| `suite-08-ad7ed0` | Spelling correction | 132.9s |
| `suite-09-f85ec3` | Barge-in | 98.0s |
| `suite-10-fd7cf1` | Ambiguous request | 161.0s |
| `suite-11-1cd272` | Human handoff | 53.5s |

## Strongest Calls

These calls have the clearest combination of natural flow, complete evidence, and meaningful bug signal:

- `suite-02-38df50`: appointment cancellation with insufficient identity verification.
- `suite-07-a48052`: urgent chest-symptom guidance arrived too late.
- `suite-11-1cd272`: direct request for a person routes to the test line and disconnects.
- `suite-05-703332`: insurance question is not answered and ends in failed transfer.
- `suite-03-35700e`: weekend-hours scenario surfaces scheduling and transfer issues.
- `suite-08-ad7ed0`: spelling correction tests uncommon-name handling.
- `suite-10-fd7cf1`: ambiguous request shows clarification followed by failed scheduling/transfer.
- `suite-09-f85ec3`: intentional barge-in still produces useful wrong-record/transfer evidence.

## Calls To Recheck Manually

These calls are usable, but should get a human listening pass before final submission:

- `d8280b05d6`: good appointment-booking evidence, but the caller says "let me pick the time that fits best for you," which sounds more like staff than a patient. This call also has the only detected pause over 4 seconds.
- `suite-06-34923a`: useful failed-transfer evidence, but the caller asks some logistics questions after the test-line goodbye.
- `suite-04-e132e4`: useful refill workflow bug, but the caller briefly uses clinic-like wording.
- `suite-01-42cb01`: useful wrong-record evidence, but the call does not get deeply into rescheduling because the agent gets stuck in lookup.

## Recommendation

The current submission is viable because it includes enough complete calls, recordings, transcripts, and a bug report with strong issues. For a stronger final impression, rerun only the weakest scenarios instead of rerunning the whole suite:

1. `appointment-simple`
2. `office-logistics`
3. optional: `medication-refill`

If no reruns are done, submit all 12 calls but lead the Loom walkthrough and bug report with the strongest calls listed above.
