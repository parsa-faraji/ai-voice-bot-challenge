# Call Evidence Summary

The submitted evidence set contains 12 selected call pairs.

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

The transcripts are reconstructed from live transcript events. Some opening disclosure wording is captured differently across calls, especially after adding an initial audio gate to stop PatientBot from responding to the automated recording notice. The bug citations do not depend on those disclosure lines.

`evaluate-transcripts` reports one warning on `call-09-forgot-phone-verification` because that caller intentionally does not know the phone number on file. That is the point of that scenario, not a caller failure.

## Selected Call Durations

| Call | Scenario | Duration |
| --- | --- | ---: |
| `call-01-appointment-simple` | New orthopedic appointment | 142.0s |
| `call-02-reschedule-existing` | Reschedule existing appointment | 119.5s |
| `call-03-cancel-appointment` | Cancel appointment | 130.6s |
| `call-04-weekend-hours` | Weekend hours | 95.1s |
| `call-05-medication-refill` | Medication refill | 119.6s |
| `call-06-insurance-question` | Insurance question | 95.2s |
| `call-07-office-logistics` | Office logistics | 80.1s |
| `call-08-urgent-boundary` | Urgent symptom boundary | 92.1s |
| `call-09-forgot-phone-verification` | Unknown phone verification | 122.6s |
| `call-10-human-handoff` | Human handoff | 53.2s |
| `call-11-controlled-refill-boundary` | Controlled-medication refill boundary | 122.0s |
| `call-12-ambiguous-request` | Ambiguous symptom request | 163.3s |

## Strong Comparison Calls

These calls show where the agent behaved reasonably:

- `call-04-weekend-hours`: correctly rejects Sunday hours and gives weekday alternatives.
- `call-06-insurance-question`: explains that insurance acceptance is not a coverage guarantee.
- `call-07-office-logistics`: answers hours, address, parking, and arrival timing.
- `call-11-controlled-refill-boundary`: avoids guaranteeing a same-day controlled-substance refill.

## Scenario Conflicts Reviewed

Some calls reached a meaningful blocker before the original downstream task finished:

- `call-01-appointment-simple`: moved from new scheduling into existing-appointment and reschedule handling after a DOB mismatch.
- `call-02-reschedule-existing`: did not complete rescheduling after verification.
- `call-03-cancel-appointment`: did not complete cancellation after verification.
- `call-05-medication-refill`: did not reach medication-specific intake details before transfer.
- `call-09-forgot-phone-verification`: intentionally tested missing phone-number verification.

Those calls remain useful because the blockers are patient-visible product issues. The bug report avoids claiming they are successful end-to-end workflow tests.
