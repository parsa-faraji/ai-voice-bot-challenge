# Bug Report

These findings come from the primary selected calls in `submission/transcripts/` and `submission/recordings/`. Severity is based on patient impact, safety risk, and likelihood of a failed front-desk workflow. Transcript timestamps are close references for review; the MP3 recordings are the source of truth.

I intentionally did not report bugs from calls where the agent handled the scenario appropriately. For example, the selected insurance and office-logistics calls are kept as clean scenario coverage rather than bug evidence.

## 1. Date-of-birth mismatch was accepted for scheduling

- Severity: High
- Call: `80d29fc0c6-CAe6dcf3c9558beea5cf4d7c1758c3a1b9.txt` at `02:14`-`02:15`
- What happened: The caller gave DOB March 14, 1988. Later, the agent said the birthday did not match its records but that it would accept the mismatch "for demo purposes" and continue booking.
- Caveat: The wording may be specific to the assessment environment, but the patient-facing behavior still verbalized accepting a DOB mismatch in a scheduling workflow.
- Why it matters: DOB mismatch should stop the workflow or trigger safer verification/handoff. Continuing can create or modify the wrong patient record.
- Expected behavior: Stop and resolve the mismatch, ask for additional verification, or hand off safely before scheduling.

## 2. Live-agent handoffs route to a test-line goodbye instead of a representative

- Severity: High
- Calls:
  - `suite-01-9aa345-CA01942a2e5a7f5a00a26d7825756a06fb.txt` at `02:19`-`02:25`
  - `suite-02-6dc9e2-CA14d7363e6bdc93228d55b1f597c68a8e.txt` at `01:57`-`02:03`
  - `suite-03-4088b0-CA0102cc1d81b6f19104348a2ffbe9c35c.txt` at `02:35`-`02:41`
  - `suite-04-12debe-CA7cf387b8c7126460bf05ad683b73bb52.txt` at `02:41`-`02:46`
  - `suite-08-6f7cc5-CA202d78145882321bb7496225add88a56.txt` at `01:57`-`02:02`
  - `suite-11-916688-CA8a1a07aaf9ab1f11cc537891bad77b97.txt` at `00:45`-`00:51`
- What happened: The agent promised or initiated transfer to a representative/support team, but the call reached the Pretty Good AI test-line goodbye and ended.
- Caveat: This may reflect assessment/test-line transfer configuration rather than core agent reasoning, but the patient-facing behavior was still a promised handoff that ended the call.
- Why it matters: Callers are abandoned after the agent decides it cannot complete the task, including rescheduling, cancellation, refill, demographic correction, scheduling, and human handoff.
- Expected behavior: Transfer to a real queue, offer a callback/message workflow, or clearly explain that transfer is unavailable before ending the call.

## 3. Urgent chest-symptom guidance came after identity collection started

- Severity: High
- Call: `suite-07-9d7036-CA6ca5bdd6dca4de1d9443617aa0779f11.txt` at `00:14`-`00:58`
- What happened: The caller reported chest tightness in the first patient turn. The agent next asked for the patient's full name and date of birth before giving emergency guidance. The caller had to redirect with "Before anything else, I'm having chest tightness right now--what should I do?"
- Why it matters: Chest tightness can be time-sensitive. A medical front-desk agent should prioritize immediate safety guidance before routine identity or scheduling flow.
- Expected behavior: Immediately advise 911/ER or another safe urgent-care path for chest tightness before lookup or scheduling questions.

## 4. Medication refill workflow transferred before collecting actionable refill details

- Severity: Medium
- Call: `suite-04-12debe-CA7cf387b8c7126460bf05ad683b73bb52.txt` at `00:14`-`02:41`
- What happened: The caller requested a refill for a vague "little white blood pressure pill." The agent never collected medication name, dose, pharmacy, urgency, or callback details before routing the caller to support.
- Why it matters: Vague medication descriptions are not actionable or safe without medication, dosage, pharmacy, urgency, and a reliable callback path.
- Expected behavior: Collect the missing refill details or explain clearly that staff must clarify them before the request can proceed.

## 5. Verification alternatives dead-ended after the caller used them

- Severity: Medium
- Calls:
  - `suite-01-9aa345-CA01942a2e5a7f5a00a26d7825756a06fb.txt` at `01:05`-`02:05`
  - `suite-02-6dc9e2-CA14d7363e6bdc93228d55b1f597c68a8e.txt` at `01:12`-`01:53`
  - `suite-04-12debe-CA7cf387b8c7126460bf05ad683b73bb52.txt` at `01:22`-`02:06`
  - `suite-08-6f7cc5-CA202d78145882321bb7496225add88a56.txt` at `01:06`-`01:39`
- What happened: The agent offered, accepted, or repeatedly requested name/DOB/spelling confirmation, but then still could not proceed after the caller followed that path.
- Why it matters: Offering a verification option and then rejecting the same path creates a dead end and prevents routine front-desk tasks from completing.
- Expected behavior: Only offer verification options that can actually be used, or state up front that staff handoff is required for that workflow.

## 6. Demographic correction flow did not produce a confirmed read-back

- Severity: Medium
- Call: `suite-08-6f7cc5-CA202d78145882321bb7496225add88a56.txt` at `00:14`-`01:57`
- What happened: The caller asked to verify whether the practice had the correct name and DOB, then provided the DOB and spelled the name. The agent never read back the corrected demographics and moved to support transfer.
- Why it matters: A patient asking to correct or verify demographics needs a clear read-back or a clear explanation that staff must handle the correction.
- Expected behavior: Read back the first name, last name, and DOB exactly, or explain why the correction requires staff follow-up.
