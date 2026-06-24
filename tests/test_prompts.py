from voicebot.prompts import (
    build_patient_instructions,
    format_phone_for_speech,
    opening_response_instruction,
)
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

    assert "Do not prepend filler before answering" in instructions
    assert "let's sort that out together" in instructions


def test_prompt_requires_direct_spelling_without_preface():
    instructions = build_patient_instructions(get_scenario("controlled-refill-boundary"))

    assert "produce exactly one spoken patient response" in instructions
    assert "answer only with the spelling" in instructions
    assert "Marcus, spelled M A R C U S, Hill, spelled H I L L" in instructions
    assert 'Do not say "let me spell that"' in instructions


def test_prompt_keeps_natural_turn_taking_unless_edge_case():
    instructions = build_patient_instructions(
        get_scenario("appointment-simple"),
        caller_phone="+18339589786",
    )

    assert "Do not fight normal verification" in instructions
    assert "You do NOT have to finish identity verification" not in instructions
    assert "Answer one question at a time" in instructions
    assert "Do not bundle name, DOB, spelling, phone, insurance" in instructions
    assert "Do not interrupt or talk over the agent unless" in instructions
    assert "833-958-9786" in instructions
    assert "do not say you do not know the phone number" in instructions.lower()


def test_prompt_handles_dob_before_identity_is_established():
    instructions = build_patient_instructions(get_scenario("cancel-appointment"))

    assert "If your name has not been established" in instructions
    assert "This is Elena Garcia, date of birth November 21, 1991" in instructions


def test_prompt_marks_single_unknown_phone_scenario():
    instructions = build_patient_instructions(get_scenario("forgot-phone-verification"))

    assert "one scenario where you do not know" in instructions
    assert "offer name, DOB, and spelling instead" in instructions


def test_phone_format_for_speech():
    assert format_phone_for_speech("+18339589786") == "833-958-9786"


def test_patient_prompt_uses_patient_intent_not_test_language():
    instructions = build_patient_instructions(get_scenario("holiday-provider-edge"))

    assert "Test whether" not in instructions
    assert "Find an appointment next week" in instructions
