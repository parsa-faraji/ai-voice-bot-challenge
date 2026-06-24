# Call Evidence Summary

The final submission set contains 12 selected call pairs in `submission/recordings/` and `submission/transcripts/`. Every selected call has both an MP3 recording and a speaker-labeled transcript.

## Checks Performed

- Confirmed all selected calls target only `+18054398008`.
- Confirmed all selected calls use the same caller number documented in `SUBMISSION.md`.
- Confirmed every selected transcript has a matching MP3 recording.
- Ran `uv run voicebot evaluate-transcripts submission/transcripts` to screen for patient-bot issues.
- Ran `ffprobe` duration checks on the selected MP3 files.

## Selected Call Durations

| Run | Scenario | Duration |
| --- | --- | ---: |
| `80d29fc0c6` | New appointment | 154.0s |
| `suite-01-9aa345` | Reschedule existing appointment | 146.8s |
| `8ab7a69965` | Cancel appointment | 134.7s |
| `suite-03-4088b0` | Weekend hours | 162.0s |
| `suite-04-12debe` | Medication refill | 167.8s |
| `suite-05-31dab8` | Insurance question | 95.2s |
| `suite-06-e55a17` | Office logistics | 80.1s |
| `suite-07-9d7036` | Urgent symptom boundary | 92.1s |
| `suite-08-6f7cc5` | Name/DOB correction | 124.4s |
| `suite-11-916688` | Human handoff | 53.9s |
| `26a95f83ee` | Controlled-medication refill boundary | 117.8s |
| `dce98865d9` | Holiday and unknown-provider scheduling | 131.2s |

## Strong Caller-Quality Calls

These calls are especially clean from a caller-quality perspective and should be easy for reviewers to listen to:

- `suite-05-31dab8`: insurance acceptance and coverage caveat question; clean comparison coverage.
- `suite-06-e55a17`: office hours, address, parking, and arrival timing; clean comparison coverage.
- `suite-07-9d7036`: urgent symptom safety boundary; useful bug evidence and clean caller behavior.
- `26a95f83ee`: controlled-medication refill boundary; clean caller behavior and useful reinforcement for transfer/verification issues.
- `dce98865d9`: holiday and unknown-provider scheduling; clean edge coverage where the agent handled the constraint correctly.

## Review Notes

The transcript evaluator reported warning-level items in some reviewed calls, mostly around repeated verification prompts or short filler. Final bug citations are based on clear agent-side behavior and checked against the MP3 recordings.

The two newest selected probes add targeted exploration of high-risk edges: one controlled-medication request that stayed safe but still dead-ended at handoff, and one holiday/provider scheduling request that the agent handled correctly.
