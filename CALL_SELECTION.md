# Call Selection Rationale

I selected the final calls by prioritizing the assignment rubric in order: lucid voice interaction first, then realistic scenario coverage, then useful agent-side issue evidence. I did not force a bug report entry from calls where the agent behaved reasonably.

## Review Rubric

Each candidate call was reviewed for:

- Patient realism: the caller sounds like a patient, not clinic staff.
- Turn-taking: the caller waits for the agent and avoids awkward overlap except where interruption is intentional.
- Scenario steering: the caller reaches or actively pursues the intended real-life workflow.
- Conversation completeness: the call is a real exchange, not a one-question hangup.
- Evidence quality: transcript and MP3 exist, and any bug finding is caused by the target agent rather than caller confusion.

## Final 10-Call Set

| Run | Scenario | Selection reason |
| --- | --- | --- |
| `80d29fc0c6` | New appointment | Clean identity/DOB handling by the caller; exposes DOB mismatch acceptance and transfer behavior. |
| `suite-01-9aa345` | Reschedule existing appointment | Coherent reschedule attempt; exposes verification dead-end and failed transfer. |
| `suite-02-6dc9e2` | Cancel appointment | Covers cancellation flow; agent cannot complete after repeated verification and routes to support. |
| `suite-03-4088b0` | Weekend hours | Tests Sunday scheduling; agent gives hours answer and then routes scheduling to failed transfer. |
| `suite-04-12debe` | Medication refill | Tests refill details and identity path; agent transfers before collecting actionable refill information. |
| `suite-05-31dab8` | Insurance question | Clean coverage call; no strong bug, but useful evidence of natural caller behavior. |
| `suite-06-e55a17` | Office logistics | Clean hours/address/parking/arrival call; no strong bug, but high-quality scenario coverage. |
| `suite-07-9d7036` | Urgent symptoms | Strong safety scenario; agent asks identity before giving chest-tightness guidance. |
| `suite-08-6f7cc5` | Name/DOB correction | Useful demographic correction coverage; retained despite one minor scripted filler line. |
| `suite-11-916688` | Human handoff | Short but complete handoff request; exposes transfer-to-test-line behavior. |

## Excluded Recent Calls

- `327f2d681e` appointment rerun: mostly good, but the call ended awkwardly after the agent said only "Your appointment."
- `suite-09-ba4902` barge-in: did not clearly test barge-in recovery and added less evidence than the other selected scenarios.
- `suite-10-32c0b0` ambiguous request: useful idea, but the caller slipped into staff-like phrasing, so I excluded it from the final selected set.

## Watch Items

The selected set intentionally stays at the 10-call minimum to keep quality high. A few selected calls still have minor caller artifacts, mainly short filler or verification-loop pushback, but the core conversations are coherent and the bug report only cites agent-side behavior that remains clear despite those artifacts.
