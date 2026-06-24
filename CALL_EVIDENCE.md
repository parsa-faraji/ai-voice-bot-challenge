# Call Evidence Summary

The final submission set contains 12 selected call pairs.

Each selected call has:

- an MP3 recording in `submission/recordings/`
- a speaker-labeled transcript in `submission/transcripts/`

## Checks Performed

- Confirmed all selected calls target only `+18054398008`.
- Confirmed all selected calls use the caller number documented in `SUBMISSION.md`.
- Confirmed every selected transcript has a matching MP3 recording.
- Ran transcript evaluation against the selected transcript set.
- Checked recording durations with `ffprobe`.
- Reviewed the transcripts for caller-side contradictions before writing the bug report.

## Transcript Scope

The MP3 is the review source of truth.

The transcripts are reconstructed from live transcript events. A few opening disclosure lines are captured differently across calls, either as a separate line or combined with the first greeting. The bug citations do not depend on those disclosure lines.

`evaluate-transcripts` reports warning-level items on some selected calls. I reviewed those manually before citation. In the final report, caller-side warnings are treated as evidence-quality checks, not as agent bugs.

## Selected Call Durations

| Call | Scenario | Duration |
| --- | --- | ---: |
| `call-01-appointment-simple` | New appointment | 154.0s |
| `call-02-reschedule-existing` | Reschedule existing appointment | 146.8s |
| `call-03-cancel-appointment` | Cancel appointment | 134.7s |
| `call-04-weekend-hours` | Weekend hours | 162.0s |
| `call-05-medication-refill` | Medication refill | 167.8s |
| `call-06-insurance-question` | Insurance question | 95.2s |
| `call-07-office-logistics` | Office logistics | 80.1s |
| `call-08-urgent-boundary` | Urgent symptom boundary | 92.1s |
| `call-09-demographic-correction` | Name/DOB correction | 124.4s |
| `call-10-human-handoff` | Human handoff | 53.9s |
| `call-11-controlled-refill-boundary` | Controlled-medication refill boundary | 117.8s |
| `call-12-holiday-provider-edge` | Holiday and unknown-provider scheduling | 131.2s |

## Strong Comparison Calls

These calls show where the agent behaved reasonably:

- `call-06-insurance-question`: explains that insurance acceptance is not a coverage guarantee.
- `call-07-office-logistics`: answers hours, address, parking, and arrival timing.
- `call-12-holiday-provider-edge`: rejects Sunday and July Fourth, and does not invent Dr. Xavier Novak.

## Scenario Conflicts Reviewed

Several calls reached a meaningful blocker before the intended task fully completed:

- `call-01-appointment-simple`: started as new scheduling, then became existing-appointment, DOB-mismatch, and handoff evidence.
- `call-02-reschedule-existing`: did not complete rescheduling because verification dead-ended.
- `call-03-cancel-appointment`: did not complete cancellation because verification dead-ended.
- `call-05-medication-refill`: did not fully test refill processing because verification blocked the workflow.
- `call-11-controlled-refill-boundary`: did not fully test controlled-refill processing because verification blocked the workflow.

Those calls remain useful because the blockers are patient-visible product issues. The bug report avoids claiming that these are successful end-to-end workflow tests.
