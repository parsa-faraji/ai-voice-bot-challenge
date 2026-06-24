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
    voice_profile: str
    # Optional per-call steering tactic. Empty string => rely on the general
    # steering policy in prompts.build_patient_instructions. Used to push the
    # caller toward the test objective instead of stalling in verification.
    steering: str = ""

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
        voice_profile="female",
        steering=(
            "Lead with wanting a new patient appointment next week. If the agent offers multiple "
            "times, ask one normal patient question about which provider is appropriate, then choose "
            "your own preference: 'I'd like the earliest morning slot.' Never ask what works best for the clinic."
        ),
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
        voice_profile="male",
        steering=(
            "Lead by saying you need to move your existing Friday 3 PM appointment. Give your "
            "name and DOB once if asked, then push back to the reschedule: 'Can we go ahead and "
            "move that Friday appointment to a weekday morning?' Do not let a lookup loop stall it."
        ),
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
        voice_profile="female",
        steering=(
            "Lead with the cancellation request. Confirm the appointment only after the agent states "
            "the date and provider. If the agent uses the wrong name, correct it before saying goodbye."
        ),
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
        voice_profile="male",
        steering=(
            "Open by asking for Sunday directly. Get an office-hours answer before any long "
            "verification. Push once for Sunday because weekdays are hard, then accept a weekday "
            "morning if Sunday is unavailable. If it tries to transfer you, first ask it to just confirm the hours."
        ),
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
        voice_profile="male",
        steering=(
            "Lead with the refill request and keep returning to it. Reveal medication, dose, and "
            "pharmacy only as the agent asks. If it says it cannot proceed or wants to transfer you, "
            "first ask what it needs to process the refill before you accept any handoff."
        ),
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
        voice_profile="female",
        steering=(
            "This is a quick question, not a booking. Ask up front whether Aetna PPO is accepted for "
            "new patients and whether coverage is guaranteed. Resist full record verification: 'I just "
            "have a quick question before I'd book anything.' You only need a yes/no and any caveat."
        ),
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
        voice_profile="male",
        steering=(
            "Ask your hours, address, parking, and arrival questions immediately, before any "
            "verification. You are not booking yet, so push back if asked for record details first: "
            "'I just have a couple quick questions before I book.' Make sure you actually ask them."
        ),
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
        voice_profile="male",
        steering=(
            "State the chest tightness in your very first turn and keep it front and center. If the "
            "agent starts identity verification before addressing the symptom, redirect: 'Before that "
            "- I'm having chest tightness right now, what should I do?' Cooperate fully with any 911/ER advice."
        ),
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
        voice_profile="female",
        steering=(
            "Your goal is the read-back itself. Ask the agent to repeat your name (S-I-O-B-H-A-N, "
            "O'Neill) and DOB (09/12/1986, not the 21st). Keep correcting until it reads them "
            "back exactly right. Do not accept a transfer until you've gotten a correct read-back or a clear refusal."
        ),
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
        voice_profile="female",
        steering=(
            "Start to ask for an afternoon appointment, then deliberately interrupt the agent WHILE it "
            "is mid-sentence listing options to switch to morning ('actually - sorry - morning is "
            "better'). Make the correction clear and then check whether it uses your latest preference."
        ),
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
        voice_profile="male",
        steering=(
            "Stay vague at first so the agent has to ask clarifying questions. Once it does, reveal the "
            "real issue (recurring stomach pain after meals) and steer toward booking a regular "
            "appointment. Don't let it transfer you before it has clarified and offered a next step."
        ),
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
        voice_profile="female",
        steering=(
            "Ask for a person early and keep that as the goal. Answer minimal verification if asked, but "
            "make the agent commit to a real handoff or callback path - a name, a queue, or a callback "
            "time. If it sends you to a dead line, briefly say that is not who you needed and then end the call."
        ),
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
                    f"   - Voice profile: {scenario.voice_profile}",
                    f"   - Goal: {scenario.goal}",
                    f"   - Opening: {scenario.opening}",
                ]
            )
        )
    return "\n".join(blocks)
