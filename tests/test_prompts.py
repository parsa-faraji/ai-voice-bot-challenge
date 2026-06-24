from voicebot.prompts import build_patient_instructions, opening_response_instruction
from voicebot.scenarios import get_scenario


def test_prompt_prioritizes_direct_identity_questions():
    instructions = build_patient_instructions(get_scenario("appointment-simple"))

    assert "Always answer the agent's direct question first" in instructions
    assert 'If the agent asks "Am I speaking with Maya?"' in instructions
    assert "Do not skip identity questions to force the scenario" in instructions


def test_opening_response_answers_identity_before_goal():
    instruction = opening_response_instruction(get_scenario("appointment-simple"))

    assert "answer using this example in your own voice" in instruction
    assert "Yes, this is Maya Thompson" in instruction
    assert "do not speak over its greeting" in instruction


def test_prompt_rejects_unnatural_transition_filler():
    instructions = build_patient_instructions(get_scenario("medication-refill"))

    assert "Do not prepend motivational filler before answering" in instructions
    assert "let's sort that out together" in instructions


def test_prompt_keeps_natural_turn_taking_unless_edge_case():
    instructions = build_patient_instructions(get_scenario("appointment-simple"))

    assert "Do not fight normal verification" in instructions
    assert "You do NOT have to finish identity verification" not in instructions
    assert "Answer one question at a time" in instructions
    assert "Do not bundle name, DOB, spelling, phone, insurance" in instructions
    assert "Do not interrupt or talk over the agent unless" in instructions


def test_prompt_handles_dob_before_identity_is_established():
    instructions = build_patient_instructions(get_scenario("cancel-appointment"))

    assert "If your name has not been established" in instructions
    assert "This is Elena Garcia, date of birth November 21, 1991" in instructions
