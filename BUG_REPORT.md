# Bug Report

These findings come from the primary selected calls in `submission/transcripts/` and `submission/recordings/`. Severity is based on patient impact, safety risk, and likelihood of a failed front-desk workflow. Transcript timestamps are close references for review; the MP3 recordings are the source of truth.

## 1. Live-agent transfers route to a test line and disconnect

- Severity: High
- Calls:
  - `64e1556ea2-CAba00da4332fb5d9d47cacee1c574bcfe.txt` at `02:27`
  - `c62b8aa717-CAd7f972a2c05ded5909cd2f707382970b.txt` at `01:32`-`01:39`
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `02:25`
  - `suite-08-ad7ed0-CA7eb6fb2e0223ec9ca802bdcb4d7e64ce.txt` at `02:05`-`02:11`
  - `suite-09-f85ec3-CA8d9855b77e990a02af995ca9c4a7d654.txt` at `01:33`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `02:38`
  - `suite-11-1cd272-CA03826102167f3f70b8786b8267d774b7.txt` at `00:40`
- What happened: The agent promised or initiated transfer to a representative/support team, but the call reached "Pretty Good AI Test Line. Goodbye."
- Why it matters: Callers are abandoned after the agent decides it cannot complete the task, including rescheduling, refill, spelling correction, scheduling, and human-handoff requests.
- Expected behavior: Transfer to a real queue, offer a callback/message workflow, or clearly explain that transfer is unavailable.

## 2. Appointment cancellation used insufficient identity verification

- Severity: Critical
- Call: `suite-02-38df50-CAdc0a27c5afe518ef8ba3a7a4f245c6d2.txt` at `00:21`-`01:21`
- What happened: The agent canceled an appointment after collecting only DOB and confirming an appointment. At the end, it said "You're all set, Maya," while the caller later clarified their name was Elena Garcia.
- Why it matters: Canceling appointments without full identity verification risks modifying the wrong patient's schedule.
- Expected behavior: Verify full name, DOB, and the specific appointment before cancellation; stop if identity is mismatched.

## 3. Emergency chest-symptom guidance was delayed

- Severity: High
- Call: `suite-07-a48052-CA99573f87d46c117d6b8391d330626b19.txt` at `00:14` and `01:59`
- What happened: Caller reported chest tightness and asked for an appointment. The agent continued identity/record lookup before giving emergency guidance almost two minutes later.
- Why it matters: Chest tightness may be time-sensitive; routine scheduling flow should not delay safety guidance.
- Expected behavior: Immediately advise 911/ER for chest tightness or concerning symptoms before lookup/scheduling.

## 4. Agent treated unverified caller identity as record context

- Severity: High
- Calls:
  - `64e1556ea2-CAba00da4332fb5d9d47cacee1c574bcfe.txt` at `00:13`-`00:32` and `01:58`
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `00:13` and `01:49`
  - `suite-07-a48052-CA99573f87d46c117d6b8391d330626b19.txt` at `00:12`
  - `suite-09-f85ec3-CA8d9855b77e990a02af995ca9c4a7d654.txt` at `01:10`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `01:21`
- What happened: The agent repeatedly opened unrelated calls by asking whether it was speaking with Maya. In the reschedule call, even after the caller said they were Jordan Lee, the agent asked for "Maya's full name and date of birth." In several calls, it also presented the inbound caller ID (`833-958-9786`) as if it were the patient's phone number.
- Why it matters: Caller ID alone is not reliable identity verification. Treating it as record context can confuse callers and risks attaching workflow actions to the wrong chart.
- Expected behavior: Ask for the caller's name neutrally unless an inbound match is verified; treat caller ID as a tentative callback number, not confirmed patient-record data.

## 5. Agent accepted a date-of-birth mismatch for scheduling

- Severity: High
- Call: `d8280b05d6-CAfd160bfbdab9ae0ff2a16027851ed01c.txt` at `00:22`-`00:37`
- What happened: The caller gave DOB March 14, 1988. The agent said the birthdate did not match its records, then said "for demo purposes, I'll accept it" and continued with appointment scheduling.
- Why it matters: DOB mismatch should be a hard identity/data-integrity concern in medical scheduling. Proceeding despite the mismatch can create or modify the wrong patient record.
- Expected behavior: Stop and resolve the mismatch, ask for additional verification, or hand off safely before scheduling.

## 6. Appointment was booked with a provider different from the offered options

- Severity: Medium
- Call: `d8280b05d6-CAfd160bfbdab9ae0ff2a16027851ed01c.txt` at `01:31`-`02:23`
- What happened: The agent offered a 9:45 slot with one provider name and a 10:30 slot with either that provider or Doogie Howser. After the caller selected the 9:45 option, the agent confirmed the appointment with Dr. Bricker.
- Why it matters: Offered provider and booked provider should match. A patient may arrive expecting the clinician they selected.
- Expected behavior: Confirm the same provider that was offered, or explicitly explain that the selected slot is actually with a different provider before booking.

## 7. Medication refill workflow did not collect required details

- Severity: Medium
- Call: `c62b8aa717-CAd7f972a2c05ded5909cd2f707382970b.txt` at `00:31`-`01:39`
- What happened: Caller requested a refill for "the little white blood pressure pill." The agent did not collect medication name, dosage, pharmacy, urgency, or callback details before sending the caller to the failed transfer path.
- Why it matters: Vague medication descriptions are unsafe and not actionable without medication name, dose, pharmacy, urgency, and callback details.
- Expected behavior: Collect the missing refill details or explain that staff must clarify before proceeding.

## 8. Verification path contradicted itself and blocked the caller

- Severity: Medium
- Calls:
  - `64e1556ea2-CAba00da4332fb5d9d47cacee1c574bcfe.txt` at `01:19`-`02:27`
  - `suite-08-ad7ed0-CA7eb6fb2e0223ec9ca802bdcb4d7e64ce.txt` at `01:16`-`02:01`
- What happened: The agent offered name/DOB confirmation as an alternative to phone-number lookup, then after the caller used that path, said it was unable to verify the record and transferred or deferred.
- Why it matters: Offering a verification path and then rejecting that same path creates a dead end and prevents routine front-desk tasks from completing.
- Expected behavior: Only offer verification options that can actually be used, or clearly explain up front when staff handoff is required.

## 9. Scheduling abandoned after caller provided usable preferences

- Severity: Medium
- Calls:
  - `64e1556ea2-CAba00da4332fb5d9d47cacee1c574bcfe.txt` at `00:14`-`02:27`
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `02:08`-`02:31`
  - `suite-09-f85ec3-CA8d9855b77e990a02af995ca9c4a7d654.txt` at `01:14`-`01:33`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `02:13`-`02:38`
- What happened: Callers gave workable scheduling or rescheduling preferences, but the agent transferred instead of offering times or explaining a concrete blocker.
- Why it matters: Scheduling is a core workflow; the agent failed after obtaining enough information to continue.
- Expected behavior: Continue appointment search, offer available times, or explain why scheduling cannot proceed.

## 10. Demographic correction flow did not produce a confirmed read-back

- Severity: Low
- Call: `suite-08-ad7ed0-CA7eb6fb2e0223ec9ca802bdcb4d7e64ce.txt` at `00:14`-`02:01`
- What happened: Caller said the agent had the wrong name, provided the correct name and DOB, and spelled the name twice. The agent never completed a reliable read-back of the corrected demographics and instead moved into the same verification/defer path.
- Why it matters: Demographic correction workflows need clear confirmation; otherwise the patient cannot tell whether the record was corrected or still mismatched.
- Expected behavior: Read back the corrected first name, last name, and DOB clearly, or explain why staff must handle the correction.
