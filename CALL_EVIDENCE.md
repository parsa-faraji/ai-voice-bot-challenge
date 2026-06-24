# Call Evidence Summary

The final submission set contains 10 selected call pairs in `submission/recordings/` and `submission/transcripts/`. Every selected call has both an MP3 recording and a speaker-labeled transcript.

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
| `suite-02-6dc9e2` | Cancel appointment | 124.6s |
| `suite-03-4088b0` | Weekend hours | 162.0s |
| `suite-04-12debe` | Medication refill | 167.8s |
| `suite-05-31dab8` | Insurance question | 95.2s |
| `suite-06-e55a17` | Office logistics | 80.1s |
| `suite-07-9d7036` | Urgent symptom boundary | 92.1s |
| `suite-08-6f7cc5` | Name/DOB correction | 124.4s |
| `suite-11-916688` | Human handoff | 53.9s |

## Clean Coverage Calls

These calls are kept primarily because they show realistic, coherent patient behavior across common front-desk workflows:

- `suite-05-31dab8`: insurance acceptance and coverage caveat question.
- `suite-06-e55a17`: office hours, address, parking, and arrival timing.
- `suite-07-9d7036`: urgent symptom safety boundary.

## Review Notes

The transcript evaluator reported warning-level items in some selected calls, mostly around repeated verification prompts or short filler. I did not use those caller-side artifacts as bug evidence. Calls with stronger patient-bot contamination were excluded from the selected set.
