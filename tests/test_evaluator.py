from pathlib import Path

from voicebot.evaluator import evaluate_path, evaluate_transcript, parse_transcript


def write_transcript(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "transcript.txt"
    path.write_text(
        "\n".join(
            [
                "Call transcript: test",
                "Speakers: PatientBot is this caller; AthenaAgent is the assessment target.",
                "",
                body.strip(),
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def test_parse_transcript_lines(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:13] AthenaAgent: Am I speaking with Maya?
[00:14] PatientBot: No, this is Riley Martinez.
""",
    )

    lines = parse_transcript(path)

    assert len(lines) == 2
    assert lines[0].speaker == "AthenaAgent"
    assert lines[1].timestamp == "00:14"


def test_parse_transcript_lines_with_subsecond_timestamps(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:13.4] AthenaAgent: Am I speaking with Maya?
[00:14.2] PatientBot: No, this is Riley Martinez.
""",
    )

    lines = parse_transcript(path)

    assert lines[0].elapsed_seconds == 13.4
    assert lines[1].timestamp == "00:14.2"


def test_flags_missing_identity_answer(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:13] AthenaAgent: Am I speaking with Maya?
[00:14] PatientBot: Hi, I need to cancel my appointment.
""",
    )

    findings = evaluate_transcript(path)

    assert [finding.rule for finding in findings] == ["identity-not-answered"]


def test_flags_identity_answer_after_goal(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:13] AthenaAgent: Am I speaking with Maya?
[00:14] PatientBot: Hi, I need to move an appointment. I am not Maya, this is Jordan Lee.
""",
    )

    findings = evaluate_transcript(path)

    assert [finding.rule for finding in findings] == ["identity-not-first"]


def test_flags_unhelpful_patient_voice_patterns(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:13] AthenaAgent: Please provide your date of birth.
[00:14] PatientBot: Okay, let me give you what you need so we can keep this moving.
[00:15] PatientBot: July 9, 1976.
""",
    )

    rules = {finding.rule for finding in evaluate_transcript(path)}

    assert "delayed-dob-answer" in rules
    assert "unnatural-filler" in rules


def test_accepts_confirmation_answer_to_dob_confirmation(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:13] AthenaAgent: To confirm, your date of birth is July 9, 1976. Is that correct?
[00:14] PatientBot: Yes, that is correct.
""",
    )

    assert evaluate_transcript(path) == []


def test_flags_substantive_content_after_goodbye(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:46] AthenaAgent: Hello, you've reached the Pretty Good AI Test Line. Goodbye.
[00:48] PatientBot: I still need my oxycodone refill today, and I need someone to tell me if I can take extra pills until the doctor calls.
""",
    )

    findings = evaluate_transcript(path)

    assert [finding.rule for finding in findings] == ["substantive-after-goodbye"]


def test_accepts_brief_failed_transfer_reaction(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:46] AthenaAgent: Hello, you've reached the Pretty Good AI Test Line. Goodbye.
[00:48] PatientBot: Wait, I was trying to reach a real person.
""",
    )

    assert evaluate_transcript(path) == []


def test_accepts_brief_farewell_after_goodbye(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:46] AthenaAgent: Hello, you've reached the Pretty Good AI Test Line. Goodbye.
[00:48] PatientBot: Okay, thanks for your time. Goodbye.
""",
    )

    assert evaluate_transcript(path) == []


def test_evaluate_directory(tmp_path):
    write_transcript(
        tmp_path,
        """
[00:13] AthenaAgent: Am I speaking with Maya?
[00:14] PatientBot: No, this is Riley Martinez.
""",
    )

    assert evaluate_path(tmp_path) == []


def test_flags_phone_number_not_provided(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:58] AthenaAgent: Can you please confirm the phone number you have on file with us?
[00:59] PatientBot: I don't remember which number is on file.
""",
    )

    findings = evaluate_transcript(path)

    assert [finding.rule for finding in findings] == ["phone-number-not-provided"]


def test_accepts_phone_number_answer(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:58] AthenaAgent: Can you please confirm the phone number you have on file with us?
[00:59] PatientBot: 833-958-9786.
""",
    )

    assert evaluate_transcript(path) == []


def test_accepts_phone_number_confirmation(tmp_path):
    path = write_transcript(
        tmp_path,
        """
[00:58] AthenaAgent: I have your phone number as 833-958-9786. Is that correct?
[00:59] PatientBot: Yes, that's correct.
""",
    )

    assert evaluate_transcript(path) == []
