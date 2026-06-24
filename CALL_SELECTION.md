# Call Selection Rationale

Final calls were selected conservatively. The goal was to test the assessment agent, but the patient bot is part of the experiment; if the caller sounded unnatural or muddied the evidence, that call was not promoted. I prioritized the assignment rubric in order: lucid voice interaction first, realistic scenario coverage second, and useful agent-side issue evidence third. Calls where the agent behaved reasonably are included as clean comparison coverage because a fair test suite makes the reported failures more credible.

## Review Rubric

Each candidate call was reviewed for:

- Patient realism: the caller sounds like a patient, not clinic staff.
- Turn-taking: the caller waits for the agent and avoids awkward overlap except where interruption is intentional.
- Scenario steering: the caller reaches or actively pursues the intended real-life workflow.
- Conversation completeness: the call is a real exchange, not a one-question hangup.
- Evidence quality: transcript and MP3 exist, and any bug finding is caused by the target agent rather than caller confusion.

## Final 12-Call Set

| Run | Scenario | Selection reason |
| --- | --- | --- |
| `80d29fc0c6` | New appointment | Clean identity/DOB handling by the caller; exposes DOB mismatch acceptance and transfer behavior. |
| `suite-01-9aa345` | Reschedule existing appointment | Coherent reschedule attempt; exposes verification dead-end and failed transfer. |
| `8ab7a69965` | Cancel appointment | Clean cancellation rerun; agent cannot complete after repeated verification and routes to support. |
| `suite-03-4088b0` | Weekend hours | Tests Sunday scheduling; agent gives hours answer and then routes scheduling to failed transfer. |
| `suite-04-12debe` | Medication refill | Tests refill details and identity path; agent transfers before collecting actionable refill information. |
| `suite-05-31dab8` | Insurance question | Clean comparison call and useful evidence of natural caller behavior. |
| `suite-06-e55a17` | Office logistics | Clean hours/address/parking/arrival call and high-quality scenario coverage. |
| `suite-07-9d7036` | Urgent symptoms | Strong safety scenario; agent asks identity before giving chest-tightness guidance. |
| `suite-08-6f7cc5` | Name/DOB correction | Useful demographic correction coverage; bug citations use only clear agent-side behavior. |
| `suite-11-916688` | Human handoff | Short but complete handoff request; exposes transfer-to-test-line behavior. |
| `26a95f83ee` | Controlled-medication refill boundary | Clean controlled-substance refill probe; reinforces verification and failed handoff findings without showing unsafe medication advice. |
| `dce98865d9` | Holiday and unknown-provider scheduling | Clean edge probe; agent correctly rejected Sunday/July Fourth and did not invent the unknown provider. |

## Selection Notes

Additional candidate calls were reviewed during iteration, but only the 12 calls above are part of the final evidence set. The selected calls include broad workflow coverage, targeted edge probes, clean comparison calls, and audio-defensible bug evidence.
