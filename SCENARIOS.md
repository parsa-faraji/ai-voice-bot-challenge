# Call Scenarios

The built-in suite defines 12 scenario types so the caller covers the required workflows and has room to discard weak calls while still submitting at least 10 strong conversations. The current primary submission set contains 12 call pairs after targeted reruns and quality review.

Run:

```bash
uv run voicebot scenarios
```

The built-in scenarios cover:

1. Simple new appointment scheduling
2. Rescheduling an existing appointment
3. Canceling without rescheduling
4. Weekend or closed-hours scheduling
5. Medication refill with initially missing details
6. Insurance acceptance and coverage guarantee question
7. Office hours, location, parking, and arrival logistics
8. Urgent symptom triage boundary
9. Name and DOB spelling correction
10. Interruption and barge-in behavior
11. Ambiguous hesitant request
12. Frustrated patient requesting human handoff
