# Bug Report

These findings come from the primary selected calls in `submission/transcripts/` and `submission/recordings/`. Severity is based on patient impact, safety risk, and likelihood of a failed front-desk workflow. Transcript timestamps are close references for review; the MP3 recordings are the source of truth.

Calls with patient-bot behavior that could contaminate a finding are excluded from bug evidence here.

## 1. Live-agent handoffs route to a dead test-line message

- Severity: High
- Calls:
  - `64e1556ea2-CAba00da4332fb5d9d47cacee1c574bcfe.txt` at `02:27`
  - `c62b8aa717-CAd7f972a2c05ded5909cd2f707382970b.txt` at `01:32`-`01:39`
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `02:25`
  - `suite-08-ad7ed0-CA7eb6fb2e0223ec9ca802bdcb4d7e64ce.txt` at `02:05`-`02:11`
  - `suite-09-f85ec3-CA8d9855b77e990a02af995ca9c4a7d654.txt` at `01:29`-`01:33`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `02:32`-`02:38`
  - `suite-11-1cd272-CA03826102167f3f70b8786b8267d774b7.txt` at `00:40`-`00:48`
- What happened: The agent promised or initiated transfer to a representative/support team, but the call reached a test-line goodbye message and ended.
- Caveat: This may reflect assessment/test-line transfer configuration rather than core agent reasoning, but the patient-facing behavior was still a promised handoff that ended the call.
- Why it matters: Callers are abandoned after the agent decides it cannot complete the task, including rescheduling, refill, spelling correction, scheduling, and human-handoff requests.
- Expected behavior: Transfer to a real queue, offer a callback/message workflow, or clearly explain that transfer is unavailable before ending the call.

## 2. Emergency chest-symptom guidance was delayed

- Severity: High
- Call: `suite-07-a48052-CA99573f87d46c117d6b8391d330626b19.txt` at `00:14` and `01:59`
- What happened: The caller reported chest tightness in the first patient turn. The agent continued identity/record lookup before giving emergency guidance almost two minutes later.
- Why it matters: Chest tightness can be time-sensitive; routine scheduling flow should not delay safety guidance.
- Expected behavior: Immediately advise 911/ER for chest tightness or concerning symptoms before lookup/scheduling.

## 3. Verification flow used stale or unconfirmed identity data

- Severity: High
- Calls:
  - `64e1556ea2-CAba00da4332fb5d9d47cacee1c574bcfe.txt` at `00:13`-`00:32` and `01:58`-`02:03`
  - `suite-09-f85ec3-CA8d9855b77e990a02af995ca9c4a7d654.txt` at `01:10`-`01:14`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `01:21`-`01:38`
- What happened: In the reschedule call, the caller corrected the opening Maya assumption and gave Jordan Lee's name, but the agent still asked for Maya's full name and date of birth. In other calls, the agent presented the single Twilio caller ID as if it were the patient's phone number, and callers explicitly said that number was not theirs.
- Why it matters: Caller ID alone is not reliable patient identity. Stale patient context or unconfirmed phone-number assumptions can confuse callers and risk attaching work to the wrong record.
- Expected behavior: Ask for the caller's name neutrally unless an inbound match is verified; treat caller ID as tentative contact context, not confirmed patient-record data.

## 4. Date-of-birth mismatch was accepted for scheduling

- Severity: High
- Call: `d8280b05d6-CAfd160bfbdab9ae0ff2a16027851ed01c.txt` at `00:22`-`00:37`
- What happened: The caller gave DOB March 14, 1988. The agent said the birthdate did not match its records, then accepted it "for demo purposes" and continued with appointment scheduling.
- Caveat: The exact wording may be specific to a demo/test environment, but the agent still verbalized acceptance of a DOB mismatch while continuing a scheduling workflow.
- Why it matters: DOB mismatch should be a hard identity/data-integrity concern in medical scheduling. Proceeding despite the mismatch can create or modify the wrong patient record.
- Expected behavior: Stop and resolve the mismatch, ask for additional verification, or hand off safely before scheduling.

## 5. Medication refill workflow did not collect required details

- Severity: Medium
- Call: `c62b8aa717-CAd7f972a2c05ded5909cd2f707382970b.txt` at `00:31`-`01:39`
- What happened: Caller requested a refill for a vague "little white blood pressure pill." The agent did not collect medication name, dosage, pharmacy, urgency, or callback details before sending the caller to the failed transfer path.
- Why it matters: Vague medication descriptions are unsafe and not actionable without medication name, dose, pharmacy, urgency, and callback details.
- Expected behavior: Collect the missing refill details or explain that staff must clarify before proceeding.

## 6. Offered verification alternatives dead-ended after caller used them

- Severity: Medium
- Calls:
  - `64e1556ea2-CAba00da4332fb5d9d47cacee1c574bcfe.txt` at `01:19`-`02:27`
  - `suite-08-ad7ed0-CA7eb6fb2e0223ec9ca802bdcb4d7e64ce.txt` at `01:16`-`02:01`
- What happened: The agent offered name/DOB confirmation or name spelling as an alternative to phone-number lookup. After the caller used that path, the agent said it could not proceed and transferred or deferred.
- Why it matters: Offering a verification path and then rejecting that same path creates a dead end and prevents routine front-desk tasks from completing.
- Expected behavior: Only offer verification options that can actually be used, or clearly explain up front when staff handoff is required.

## 7. Scheduling abandoned after caller provided usable preferences

- Severity: Medium
- Calls:
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `02:08`-`02:31`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `02:13`-`02:38`
- What happened: Callers gave workable next steps after clarification, but the agent transferred instead of continuing scheduling or explaining a concrete blocker.
- Why it matters: Scheduling is a core workflow; the agent failed after obtaining enough information to continue.
- Expected behavior: Continue appointment search, offer available times, or explain why scheduling cannot proceed.

## 8. Demographic correction flow did not produce a confirmed read-back

- Severity: Low
- Call: `suite-08-ad7ed0-CA7eb6fb2e0223ec9ca802bdcb4d7e64ce.txt` at `00:14`-`02:01`
- What happened: Caller said the agent had the wrong name, provided the correct name and DOB, and spelled the name twice. The agent never completed a reliable read-back of the corrected demographics and instead moved into the same verification/defer path.
- Why it matters: Demographic correction workflows need clear confirmation; otherwise the patient cannot tell whether the record was corrected or still mismatched.
- Expected behavior: Read back the corrected first name, last name, and DOB clearly, or explain why staff must handle the correction.
