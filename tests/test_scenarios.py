from voicebot.scenarios import all_scenarios, get_scenario


def test_has_standout_suite_size():
    assert len(all_scenarios()) == 12


def test_scenario_ids_are_unique():
    ids = [scenario.id for scenario in all_scenarios()]
    assert len(ids) == len(set(ids))


def test_scenarios_have_voice_profiles():
    profiles = {scenario.voice_profile for scenario in all_scenarios()}
    assert profiles == {"female", "male"}


def test_scenarios_have_first_turn_examples():
    for scenario in all_scenarios():
        assert scenario.patient_name in scenario.first_turn_example
        assert len(scenario.first_turn_example) < 140


def test_get_scenario():
    assert get_scenario("weekend-hours").title == "Weekend and closed-hours edge case"
