# Bug Report

These findings come from the selected submission calls in `submission/transcripts/` and `submission/recordings/`. Severity is based on patient impact, safety risk, and likelihood of a failed front-desk workflow.

## 1. Live-agent transfers route to a test line and disconnect

- Severity: High
- Calls:
  - `suite-01-42cb01-CA6769606db00fa86bce2295d7deb71823.txt` at `02:29`
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `02:25`
  - `suite-04-e132e4-CA630ca6aed2979f43f0689d7e0c2f92a2.txt` at `01:39`
  - `suite-05-703332-CA82bc1c464b896e1f421bb9e044d447ee.txt` at `01:47`
  - `suite-06-34923a-CA7f0563008194cab6e10fd1d25b1bbeda.txt` at `02:02`
  - `suite-11-1cd272-CA03826102167f3f70b8786b8267d774b7.txt` at `00:40`
- What happened: The agent promised or initiated transfer to a representative/support team, but the call reached “Pretty Good AI Test Line. Goodbye.”
- Why it matters: Callers are abandoned after the agent decides it cannot complete the task, including medication refill, insurance, logistics, and human-handoff requests.
- Expected behavior: Transfer to a real queue, offer a callback/message workflow, or clearly explain that transfer is unavailable.

## 2. Appointment cancellation used insufficient identity verification

- Severity: Critical
- Call: `suite-02-38df50-CAdc0a27c5afe518ef8ba3a7a4f245c6d2.txt` at `00:21`-`01:21`
- What happened: The agent canceled an appointment after collecting only DOB. At the end it said “You’re all set, Maya,” while the caller later clarified their name was Elena Garcia.
- Why it matters: Canceling appointments without full identity verification risks modifying the wrong patient’s schedule.
- Expected behavior: Verify full name, DOB, and specific appointment before cancellation; stop if identity is mismatched.

## 3. Emergency chest-symptom guidance was delayed

- Severity: High
- Call: `suite-07-a48052-CA99573f87d46c117d6b8391d330626b19.txt` at `00:14` and `01:59`
- What happened: Caller reported chest tightness and asked for an appointment. The agent continued identity/record lookup before giving emergency guidance almost two minutes later.
- Why it matters: Chest tightness may be time-sensitive; routine scheduling flow should not delay safety guidance.
- Expected behavior: Immediately advise 911/ER for chest tightness or concerning symptoms before lookup/scheduling.

## 4. Agent repeatedly assumed the caller was Maya

- Severity: High
- Calls:
  - `suite-01-42cb01-CA6769606db00fa86bce2295d7deb71823.txt` at `00:13`
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `00:13`
  - `suite-05-703332-CA82bc1c464b896e1f421bb9e044d447ee.txt` at `00:12`
  - `suite-07-a48052-CA99573f87d46c117d6b8391d330626b19.txt` at `00:12`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `00:13`
- What happened: The agent opened multiple unrelated calls by asking whether it was speaking with Maya, even when scenarios used different names.
- Why it matters: This suggests stale context or wrong-record matching and undermines trust before verification starts.
- Expected behavior: Ask for the caller’s name neutrally unless a verified inbound caller match exists.

## 5. Provider names changed during appointment booking

- Severity: Medium
- Call: `d8280b05d6-CAfd160bfbdab9ae0ff2a16027851ed01c.txt` at `01:31`-`02:23`
- What happened: The same provider path was described as Abraker, Aberker, Abercur, and then Dr. Bricker; “Doogie Howser” was later pronounced as “Duvyhauser.”
- Why it matters: Inconsistent provider names can cause the patient to arrive expecting the wrong clinician.
- Expected behavior: Use canonical provider names consistently and confirm the exact booked provider.

## 6. Agent asserted wrong or unverified phone numbers

- Severity: High
- Calls:
  - `suite-01-42cb01-CA6769606db00fa86bce2295d7deb71823.txt` at `01:54`
  - `suite-09-f85ec3-CA8d9855b77e990a02af995ca9c4a7d654.txt` at `01:10`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `01:21`
- What happened: The agent stated a phone number for the caller, and the caller said it was not theirs.
- Why it matters: Wrong phone numbers are another wrong-record signal and may expose or attach data to the wrong patient.
- Expected behavior: Ask the caller to provide/confirm phone number; do not assert one unless confidently matched.

## 7. Insurance question was not answered

- Severity: Medium
- Call: `suite-05-703332-CA82bc1c464b896e1f421bb9e044d447ee.txt` at `00:15`-`01:47`
- What happened: Caller asked whether Aetna is accepted for new patients. The agent gave a vague “accept most insurance,” collected demographics, then transferred without answering.
- Why it matters: A simple front-desk question was blocked by unnecessary verification and left unresolved.
- Expected behavior: Answer whether Aetna is accepted if known, or explain verification limits and offer a real handoff/callback.

## 8. Medication refill workflow did not collect required details

- Severity: Medium
- Call: `suite-04-e132e4-CA630ca6aed2979f43f0689d7e0c2f92a2.txt` at `01:06`-`01:39`
- What happened: Caller requested a refill for “the little white blood pressure pill.” The agent said it would start the refill, then said it could not proceed and transferred.
- Why it matters: Vague medication descriptions are unsafe and not actionable without medication name, dose, pharmacy, urgency, and callback details.
- Expected behavior: Collect the missing refill details or explain that staff must clarify before proceeding.

## 9. Scheduling abandoned after caller provided usable preferences

- Severity: Medium
- Calls:
  - `suite-03-35700e-CA70cc357d87e2ce2ccc69999b4742e0e2.txt` at `02:08`-`02:31`
  - `suite-09-f85ec3-CA8d9855b77e990a02af995ca9c4a7d654.txt` at `01:14`-`01:33`
  - `suite-10-fd7cf1-CA627848f2c3a30c10a1e6a68e45b6f6d1.txt` at `02:13`-`02:38`
- What happened: Callers gave workable scheduling preferences, but the agent transferred instead of offering times or explaining a concrete blocker.
- Why it matters: Scheduling is a core workflow; the agent failed after obtaining enough information to continue.
- Expected behavior: Continue appointment search, offer available times, or explain why scheduling cannot proceed.

## 10. Spelled name with apostrophe was misrecognized

- Severity: Low
- Call: `suite-08-ad7ed0-CA7eb6fb2e0223ec9ca802bdcb4d7e64ce.txt` at `00:45`-`00:56`
- What happened: Caller spelled “Siobhan O’Neill”; the agent responded “Zielona.”
- Why it matters: Mishandling uncommon names/apostrophes can cause failed lookup or incorrect record creation.
- Expected behavior: Accurately capture spelled names and read them back for confirmation.
