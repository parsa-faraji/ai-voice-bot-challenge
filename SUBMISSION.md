# Submission Manifest

## Phone Numbers

All live assessment calls used one caller number:

`+18339589786`

All calls targeted the assessment line:

`+18054398008`

The code is hard-locked to that target number.

## Evidence Set

The final evidence set contains 12 call pairs:

- `submission/recordings/call-01-appointment-simple.mp3`
- `submission/transcripts/call-01-appointment-simple.txt`
- matching files for `call-02` through `call-12`
- `submission/BUG_REPORT.md`

The call numbers are the review order. The names describe the intended probe, while `CALL_SELECTION.md` explains what each call actually exercised.

| Call | Intended probe | Submission role |
| --- | --- | --- |
| `call-01-appointment-simple` | New orthopedic appointment | DOB mismatch and appointment workflow evidence |
| `call-02-reschedule-existing` | Reschedule existing appointment | Verification and failed handoff evidence |
| `call-03-cancel-appointment` | Cancel appointment | Verification and failed handoff evidence |
| `call-04-weekend-hours` | Sunday/weekend hours | Clean closed-hours comparison call |
| `call-05-medication-refill` | Medication refill | Refill intake and failed handoff evidence |
| `call-06-insurance-question` | Insurance question | Clean comparison call |
| `call-07-office-logistics` | Office logistics | Clean comparison call |
| `call-08-urgent-boundary` | Urgent symptom boundary | Safety-triage evidence |
| `call-09-forgot-phone-verification` | Unknown phone on file | Alternative verification and handoff evidence |
| `call-10-human-handoff` | Human handoff | Direct handoff evidence |
| `call-11-controlled-refill-boundary` | Controlled-medication refill | Controlled-substance boundary and handoff evidence |
| `call-12-ambiguous-request` | Ambiguous symptom request | Clarification and handoff evidence |

## Review Files

- `README.md`: setup and run instructions
- `ARCHITECTURE.md`: system design and tradeoffs
- `SCENARIOS.md`: scenario coverage
- `CALL_SELECTION.md`: why each submitted call was kept
- `CALL_EVIDENCE.md`: evidence checks and call durations
- `BUG_REPORT.md`: curated findings
- `submission/`: recordings, transcripts, and submitted bug report
