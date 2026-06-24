from voicebot.scenarios import all_scenarios, get_scenario


def test_has_standout_suite_size():
    assert len(all_scenarios()) == 14


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


def test_only_one_scenario_intentionally_forgets_phone_number():
    unknown_phone = [scenario for scenario in all_scenarios() if scenario.phone_policy == "unknown"]

    assert [scenario.id for scenario in unknown_phone] == ["forgot-phone-verification"]


def test_get_scenario():
    assert get_scenario("weekend-hours").title == "Weekend and closed-hours edge case"
