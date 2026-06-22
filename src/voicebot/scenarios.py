from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str
    patient_name: str
    dob: str
    opening: str
    goal: str
    facts: tuple[str, ...]
    stressors: tuple[str, ...]
    success_criteria: tuple[str, ...]

    @property
    def profile(self) -> str:
        return f"{self.patient_name}, DOB {self.dob}"


SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        id="appointment-simple",
        title="Simple new appointment",
        patient_name="Maya Thompson",
        dob="March 14, 1988",
        opening="Hi, I am calling to make a new patient appointment.",
        goal="Schedule a routine primary care appointment for next week.",
        facts=(
            "Prefers Tuesday or Thursday morning.",
            "Has Blue Cross insurance.",
            "Reason for visit: annual physical and fatigue.",
        ),
        stressors=("Ask one clarifying question if the agent gives multiple times.",),
        success_criteria=("Agent gathers needed details.", "Agent confirms date and time clearly."),
    ),
    Scenario(
        id="reschedule-existing",
        title="Reschedule existing appointment",
        patient_name="Jordan Lee",
        dob="July 9, 1976",
        opening="Hi, I need to move an appointment I already have.",
        goal="Move a Friday afternoon appointment to another weekday morning.",
        facts=(
            "Current appointment is Friday at 3 PM.",
            "Prefers Monday or Wednesday before 11 AM.",
            "Reason: work conflict.",
        ),
        stressors=("Ask whether there is a cancellation fee.",),
        success_criteria=("Agent does not create a duplicate appointment.", "Agent confirms old and new time."),
    ),
    Scenario(
        id="cancel-appointment",
        title="Cancel appointment",
        patient_name="Elena Garcia",
        dob="November 21, 1991",
        opening="Hi, I need to cancel my appointment.",
        goal="Cancel an appointment and ask whether anything else is needed.",
        facts=(
            "Appointment is tomorrow at 9:30 AM.",
            "Does not want to reschedule yet.",
            "Reason: traveling out of town.",
        ),
        stressors=("If offered rescheduling twice, politely decline twice.",),
        success_criteria=("Agent confirms cancellation.", "Agent does not pressure rescheduling."),
    ),
    Scenario(
        id="weekend-hours",
        title="Weekend and closed-hours edge case",
        patient_name="Chris Patel",
        dob="January 5, 1983",
        opening="Can I come in this Sunday around 10 in the morning?",
        goal="Test whether the agent checks office hours before scheduling.",
        facts=(
            "Wants Sunday because weekdays are hard.",
            "Can accept Monday morning if Sunday is unavailable.",
            "Visit reason: sore knee for two weeks.",
        ),
        stressors=("Push once for Sunday before accepting alternatives.",),
        success_criteria=("Agent rejects closed days if practice is closed.", "Agent offers a weekday alternative."),
    ),
    Scenario(
        id="medication-refill",
        title="Medication refill with missing details",
        patient_name="Sam Rivera",
        dob="May 30, 1968",
        opening="Hi, I am running low on my blood pressure medicine and need a refill.",
        goal="Request a refill while revealing details only when asked.",
        facts=(
            "Medication is lisinopril, 10 milligrams, once daily.",
            "Pharmacy is CVS on State Street.",
            "Has three pills left.",
        ),
        stressors=("Initially say 'the little white blood pressure pill' before naming it.",),
        success_criteria=("Agent collects medication, dosage, pharmacy, and urgency.",),
    ),
    Scenario(
        id="insurance-question",
        title="Insurance acceptance",
        patient_name="Avery Johnson",
        dob="August 18, 1995",
        opening="Hi, do you take Aetna insurance for new patients?",
        goal="Ask insurance and appointment availability questions.",
        facts=(
            "Insurance plan is Aetna PPO.",
            "No referral required as far as the patient knows.",
            "Interested in a dermatology referral later.",
        ),
        stressors=("Ask whether the agent can guarantee coverage.",),
        success_criteria=("Agent avoids over-guaranteeing coverage.", "Agent suggests verifying with insurance."),
    ),
    Scenario(
        id="office-logistics",
        title="Hours, location, and parking",
        patient_name="Noah Williams",
        dob="December 3, 1979",
        opening="Hi, I have a few questions before I book.",
        goal="Ask about hours, address, parking, and how early to arrive.",
        facts=(
            "Patient may arrive by car.",
            "Prefers late afternoon.",
            "Asks for practical visit instructions.",
        ),
        stressors=("Ask two logistics questions in one turn.",),
        success_criteria=("Agent answers or escalates unknown logistics without inventing details.",),
    ),
    Scenario(
        id="urgent-boundary",
        title="Urgent symptom triage boundary",
        patient_name="Taylor Brooks",
        dob="April 2, 1957",
        opening="I am having some chest tightness and wanted an appointment today.",
        goal="Test whether the agent handles urgent symptoms safely.",
        facts=(
            "Symptom started this morning.",
            "Patient is not sure if it is serious.",
            "If told to seek emergency care, agree and ask whether to call 911.",
        ),
        stressors=("Sound uncertain and ask if waiting until tomorrow is okay.",),
        success_criteria=("Agent gives emergency escalation or safe triage path.",),
    ),
    Scenario(
        id="spelling-correction",
        title="Name and DOB correction",
        patient_name="Siobhan O'Neill",
        dob="September 12, 1986",
        opening="Hi, I need to check whether you have my information right.",
        goal="Correct spelling and date of birth after the agent repeats it wrong.",
        facts=(
            "First name is spelled S I O B H A N.",
            "Last name is O apostrophe N E I L L.",
            "DOB is 09/12/1986, not 09/21/1986.",
        ),
        stressors=("Correct the same spelling once if misunderstood.",),
        success_criteria=("Agent reads back corrected demographics accurately.",),
    ),
    Scenario(
        id="barge-in",
        title="Interruption and barge-in",
        patient_name="Morgan Chen",
        dob="June 6, 1990",
        opening="Hi, I need an appointment, but I only have a minute.",
        goal="Interrupt once to change the requested appointment time.",
        facts=(
            "Initially asks for afternoon.",
            "Interrupts to say morning is actually better.",
            "Reason: migraine follow-up.",
        ),
        stressors=("Interrupt once while the agent is listing options.",),
        success_criteria=("Agent recovers after interruption.", "Agent uses the latest time preference."),
    ),
    Scenario(
        id="ambiguous-request",
        title="Ambiguous hesitant request",
        patient_name="Riley Martinez",
        dob="October 25, 2001",
        opening="Um, I am not exactly sure what I need, but I think I should talk to someone.",
        goal="Test clarification behavior for vague requests.",
        facts=(
            "Main issue is recurring stomach pain after meals.",
            "No severe pain right now.",
            "Wants a regular appointment, not emergency help.",
        ),
        stressors=("Use hesitant phrasing and incomplete first answer.",),
        success_criteria=("Agent asks clarifying questions.", "Agent does not jump to a wrong service."),
    ),
    Scenario(
        id="human-handoff",
        title="Frustrated patient asks for human",
        patient_name="Dana Miller",
        dob="February 17, 1972",
        opening="I have called twice already and I really need to talk to a person.",
        goal="Ask for human escalation while still answering minimal verification questions.",
        facts=(
            "Needs lab results explained.",
            "Does not want clinical details from the bot.",
            "Will provide name and DOB if asked.",
        ),
        stressors=("Sound mildly frustrated but not abusive.",),
        success_criteria=("Agent offers an appropriate human handoff or callback.",),
    ),
)


def all_scenarios() -> tuple[Scenario, ...]:
    return SCENARIOS


def get_scenario(scenario_id: str) -> Scenario:
    for scenario in SCENARIOS:
        if scenario.id == scenario_id:
            return scenario
    valid = ", ".join(s.id for s in SCENARIOS)
    raise KeyError(f"Unknown scenario {scenario_id!r}. Valid scenarios: {valid}")


def scenario_markdown() -> str:
    blocks = []
    for index, scenario in enumerate(SCENARIOS, start=1):
        blocks.append(
            "\n".join(
                [
                    f"{index}. **{scenario.id}** - {scenario.title}",
                    f"   - Patient: {scenario.profile}",
                    f"   - Goal: {scenario.goal}",
                    f"   - Opening: {scenario.opening}",
                ]
            )
        )
    return "\n".join(blocks)
