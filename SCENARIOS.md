# Call Scenarios

The built-in suite has 14 scenario types.

The goal is coverage, not just volume. The scenarios exercise routine front-desk work, safety boundaries, and edge cases that can expose brittle agent behavior.

List the configured scenarios:

```bash
uv run voicebot scenarios
```

## Core Workflows

1. Simple new appointment scheduling
2. Rescheduling an existing appointment
3. Canceling without rescheduling
4. Medication refill with initially missing details
5. Insurance acceptance and coverage guarantee question
6. Office hours, location, parking, and arrival logistics
7. Name and DOB spelling correction

## Safety And Edge Cases

8. Urgent symptom triage boundary
9. Weekend or closed-hours scheduling
10. Controlled-medication refill safety boundary
11. Holiday, weekend, and unknown-provider scheduling
12. Interruption and barge-in behavior
13. Ambiguous hesitant request
14. Frustrated patient requesting human handoff

## Scenario Design

Each scenario includes:

- patient identity and DOB
- voice profile
- first-turn identity response
- facts to reveal only when asked
- stressors that exercise the target workflow
- success criteria for evaluating the target agent

The final submission promotes selected call pairs after review. Selection is based on call quality and evidence quality, not just whether a scenario ran.
