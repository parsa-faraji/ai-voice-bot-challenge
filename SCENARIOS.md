# Call Scenarios

The suite intentionally runs 12 calls so there is room to discard weak calls and still submit at least 10 strong conversations.

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
