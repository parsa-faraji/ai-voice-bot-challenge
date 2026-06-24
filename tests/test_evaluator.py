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
[00:48] PatientBot: Oh, okay, that is not who I needed. I was trying to reach a real person.
""",
    )

    findings = evaluate_transcript(path)

    assert [finding.rule for finding in findings] == ["substantive-after-goodbye"]


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
