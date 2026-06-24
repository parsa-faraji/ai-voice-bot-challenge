from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


TRANSCRIPT_LINE_RE = re.compile(
    r"^\[(?P<minutes>\d{2}):(?P<seconds>\d{2})(?:\.(?P<fraction>\d+))?\]\s+"
    r"(?P<speaker>[^:]+):\s*(?P<text>.*)$"
)

IDENTITY_PROMPT_RE = re.compile(r"\bam i speaking with maya\b", re.IGNORECASE)
IDENTITY_FIRST_RE = re.compile(
    r"^(hi[,.\s]+)?(yes|yeah|yep|no|nope|not maya|this is|i'm|i am|my name is)\b",
    re.IGNORECASE,
)
IDENTITY_ANSWER_RE = re.compile(
    r"\b(yes|yeah|yep|no|nope|not maya|not calling for maya|this is|i'm|"
    r"i am|my name is)\b|isn.t maya|is not maya",
    re.IGNORECASE,
)
DOB_PROMPT_RE = re.compile(r"\b(date of birth|birthdate|dob)\b", re.IGNORECASE)
DOB_ANSWER_RE = re.compile(
    r"\b(january|february|march|april|may|june|july|august|september|october|"
    r"november|december|\d{1,2}[/-]\d{1,2}|\d{4})\b",
    re.IGNORECASE,
)
PHONE_PROMPT_RE = re.compile(r"\b(phone number|number on file|phone on file)\b", re.IGNORECASE)
PHONE_ANSWER_RE = re.compile(r"\b(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b")
PHONE_UNKNOWN_RE = re.compile(
    r"\b(don't know|do not know|not sure|don't remember|do not remember|"
    r"not handy|not have|don't have|do not have|which number)\b",
    re.IGNORECASE,
)
CONFIRMATION_PROMPT_RE = re.compile(
    r"\b(confirm|make sure|correct)\b",
    re.IGNORECASE,
)
CONFIRMATION_ANSWER_RE = re.compile(
    r"\b(yes|correct|right|that's right|that is right)\b",
    re.IGNORECASE,
)
SPELL_PROMPT_RE = re.compile(r"\bspell\b.*\b(name|first|last)\b", re.IGNORECASE)
SPELL_ANSWER_RE = re.compile(r"\b[A-Z](?:[\s.-]+[A-Z]){1,}\b")
GOODBYE_RE = re.compile(r"\b(goodbye|bye|have a (great|good) day)\b", re.IGNORECASE)

UNNATURAL_FILLER_PHRASES = (
    "let's sort that out",
    "let me say that clearly",
    "let me give you the number",
    "let's keep this moving",
    "let me give you what you need",
    "let's take a quick look",
    "before we keep going",
)

STAFF_LANGUAGE_PHRASES = (
    "let me check",
    "let me think through",
    "let me pull",
    "let me pick",
    "let me confirm",
    "pull up my record",
    "i'll book",
    "i will book",
    "i'll reserve",
    "i will reserve",
    "let's get you set up",
    "set you up",
    "your preferences",
)


@dataclass(frozen=True)
class TranscriptLine:
    path: Path
    line_no: int
    elapsed_seconds: float
    speaker: str
    text: str

    @property
    def timestamp(self) -> str:
        minutes = int(self.elapsed_seconds // 60)
        seconds = self.elapsed_seconds - (minutes * 60)
        if abs(seconds - round(seconds)) < 0.05:
            return f"{minutes:02d}:{int(round(seconds)):02d}"
        return f"{minutes:02d}:{seconds:04.1f}"


@dataclass(frozen=True)
class TranscriptFinding:
    path: Path
    line_no: int
    timestamp: str
    severity: str
    rule: str
    detail: str
    excerpt: str


def evaluate_path(path: str | Path) -> list[TranscriptFinding]:
    """Evaluate one transcript file or every transcript file under a directory."""
    target = Path(path)
    if target.is_file():
        return evaluate_transcript(target)
    if not target.exists():
        raise FileNotFoundError(target)
    findings: list[TranscriptFinding] = []
    for transcript_path in sorted(target.rglob("*.txt")):
        findings.extend(evaluate_transcript(transcript_path))
    return findings


def evaluate_transcript(path: str | Path) -> list[TranscriptFinding]:
    transcript_path = Path(path)
    lines = parse_transcript(transcript_path)
    findings: list[TranscriptFinding] = []

    for index, line in enumerate(lines):
        if line.speaker == "AthenaAgent" and IDENTITY_PROMPT_RE.search(line.text):
            next_patient = _next_patient_line(lines, index)
            if next_patient is None:
                continue
            if not IDENTITY_ANSWER_RE.search(next_patient.text):
                findings.append(
                    _finding(
                        next_patient,
                        "error",
                        "identity-not-answered",
                        "PatientBot did not answer the agent's Maya identity prompt.",
                    )
                )
            elif not IDENTITY_FIRST_RE.search(next_patient.text.strip()):
                findings.append(
                    _finding(
                        next_patient,
                        "warning",
                        "identity-not-first",
                        "PatientBot answered identity only after leading with the scenario goal.",
                    )
                )

        if line.speaker == "AthenaAgent" and _is_dob_prompt(line.text):
            next_patient = _immediate_next_patient_line(lines, index)
            is_confirmation = CONFIRMATION_PROMPT_RE.search(line.text)
            answered_confirmation = (
                next_patient is not None and CONFIRMATION_ANSWER_RE.search(next_patient.text)
            )
            if next_patient and not DOB_ANSWER_RE.search(next_patient.text) and not (
                is_confirmation and answered_confirmation
            ):
                findings.append(
                    _finding(
                        next_patient,
                        "warning",
                        "delayed-dob-answer",
                        "PatientBot did not provide DOB in the first response to a DOB prompt.",
                    )
                )

        if line.speaker == "AthenaAgent" and _is_phone_prompt(line.text):
            next_patient = _immediate_next_patient_line(lines, index)
            agent_provided_phone_for_confirmation = (
                PHONE_ANSWER_RE.search(line.text) and CONFIRMATION_PROMPT_RE.search(line.text)
            )
            patient_confirmed_phone = (
                next_patient is not None
                and CONFIRMATION_ANSWER_RE.search(next_patient.text)
                and agent_provided_phone_for_confirmation
            )
            if next_patient and not PHONE_ANSWER_RE.search(next_patient.text) and not patient_confirmed_phone:
                rule = "phone-number-not-provided"
                detail = "PatientBot did not provide a phone number when the agent asked for one."
                if PHONE_UNKNOWN_RE.search(next_patient.text):
                    detail = (
                        "PatientBot said the phone number was unknown. This should be intentional, "
                        "not repeated across routine workflows."
                    )
                findings.append(_finding(next_patient, "warning", rule, detail))

        if line.speaker == "AthenaAgent" and SPELL_PROMPT_RE.search(line.text):
            next_patient = _immediate_next_patient_line(lines, index)
            agent_offered_phone_lookup = _is_phone_prompt(line.text)
            patient_answered_phone = next_patient is not None and PHONE_ANSWER_RE.search(
                next_patient.text
            )
            if (
                next_patient
                and not SPELL_ANSWER_RE.search(next_patient.text)
                and not (agent_offered_phone_lookup and patient_answered_phone)
            ):
                findings.append(
                    _finding(
                        next_patient,
                        "warning",
                        "delayed-spelling-answer",
                        "PatientBot did not spell the name in the first response to a spelling prompt.",
                    )
                )

        if line.speaker != "PatientBot":
            continue

        lower_text = line.text.lower()
        for phrase in UNNATURAL_FILLER_PHRASES:
            if phrase in lower_text:
                findings.append(
                    _finding(
                        line,
                        "warning",
                        "unnatural-filler",
                        f'PatientBot used scripted filler: "{phrase}".',
                    )
                )
        for phrase in STAFF_LANGUAGE_PHRASES:
            if phrase in lower_text:
                findings.append(
                    _finding(
                        line,
                        "warning",
                        "staff-language",
                        f'PatientBot used clinic-staff phrasing: "{phrase}".',
                    )
                )
        if len(line.text) > 260:
            findings.append(
                _finding(
                    line,
                    "warning",
                    "long-patient-turn",
                    "PatientBot turn is long enough to sound scripted or rushed.",
                )
            )

    first_agent_goodbye_index = next(
        (
            index
            for index, line in enumerate(lines)
            if line.speaker == "AthenaAgent" and GOODBYE_RE.search(line.text)
        ),
        None,
    )
    if first_agent_goodbye_index is not None:
        for line in lines[first_agent_goodbye_index + 1 :]:
            if line.speaker != "PatientBot":
                continue
            if not _is_allowed_end_reaction(line.text):
                findings.append(
                    _finding(
                        line,
                        "warning",
                        "substantive-after-goodbye",
                        "PatientBot added substantive content after the agent ended the call.",
                    )
                )

    return findings


def parse_transcript(path: str | Path) -> list[TranscriptLine]:
    transcript_path = Path(path)
    transcript_lines: list[TranscriptLine] = []
    for line_no, raw_line in enumerate(transcript_path.read_text(encoding="utf-8").splitlines(), start=1):
        match = TRANSCRIPT_LINE_RE.match(raw_line)
        if not match:
            continue
        fraction = match.group("fraction") or ""
        fractional_seconds = float(f"0.{fraction}") if fraction else 0.0
        elapsed_seconds = (
            int(match.group("minutes")) * 60
            + int(match.group("seconds"))
            + fractional_seconds
        )
        transcript_lines.append(
            TranscriptLine(
                path=transcript_path,
                line_no=line_no,
                elapsed_seconds=elapsed_seconds,
                speaker=match.group("speaker"),
                text=match.group("text").strip(),
            )
        )
    return transcript_lines


def format_findings(findings: list[TranscriptFinding]) -> str:
    if not findings:
        return "No transcript quality issues found."

    rows = []
    for finding in findings:
        rows.append(
            "\n".join(
                [
                    f"- {finding.severity.upper()} {finding.path}:{finding.line_no} "
                    f"at {finding.timestamp} [{finding.rule}]",
                    f"  {finding.detail}",
                    f"  Excerpt: {finding.excerpt}",
                ]
            )
        )
    return "\n".join(rows)


def _next_patient_line(
    lines: list[TranscriptLine], start_index: int
) -> TranscriptLine | None:
    for line in lines[start_index + 1 :]:
        if line.speaker == "PatientBot":
            return line
    return None


def _immediate_next_patient_line(
    lines: list[TranscriptLine], start_index: int
) -> TranscriptLine | None:
    if start_index + 1 >= len(lines):
        return None
    next_line = lines[start_index + 1]
    if next_line.speaker == "PatientBot":
        return next_line
    return None


def _is_dob_prompt(text: str) -> bool:
    if not DOB_PROMPT_RE.search(text):
        return False
    lowered = text.lower()
    if (
        "thanks for confirming" in lowered
        or "which would you prefer" in lowered
        or "doesn't match" in lowered
        or "does not match" in lowered
        or "mismatch" in lowered
    ):
        return False
    if SPELL_PROMPT_RE.search(text) and not (
        "correct" in lowered
        or "can you confirm your date of birth" in lowered
        or re.search(r"\b(provide|tell me|what is)\b", lowered)
    ):
        return False
    return bool(
        "?" in text
        or re.search(
            r"\b(please provide|provide your|tell me|what is|can you|could you|"
            r"confirm|is all of that correct)\b",
            lowered,
        )
    )


def _is_phone_prompt(text: str) -> bool:
    if not PHONE_PROMPT_RE.search(text):
        return False
    lowered = text.lower()
    if PHONE_ANSWER_RE.search(text) and not (
        "?" in text or "correct" in lowered or "confirm" in lowered
    ):
        return False
    return bool(
        "?" in text
        or re.search(
            r"\b(please provide|provide that number|provide the number|tell me|"
            r"use your phone number|look up your record using|number you have on file|"
            r"which would you prefer|confirm|correct|is all of that correct)\b",
            lowered,
        )
    )


def _is_allowed_end_reaction(text: str) -> bool:
    normalized = re.sub(r"[^a-z\s]", "", text.lower()).strip()
    if len(normalized) > 130:
        return False
    farewell_terms = {
        "a",
        "again",
        "appointment",
        "about",
        "anyway",
        "appreciate",
        "bye",
        "back",
        "call",
        "cancel",
        "canceling",
        "cancelling",
        "day",
        "did",
        "didnt",
        "for",
        "good",
        "goodbye",
        "help",
        "i",
        "line",
        "me",
        "my",
        "needed",
        "not",
        "ok",
        "okay",
        "person",
        "reach",
        "real",
        "refill",
        "reschedule",
        "rescheduling",
        "someone",
        "still",
        "test",
        "thank",
        "thanks",
        "that",
        "thats",
        "the",
        "this",
        "time",
        "to",
        "too",
        "trying",
        "wait",
        "was",
        "who",
        "you",
        "your",
    }
    words = set(normalized.split())
    return bool(words) and words.issubset(farewell_terms)


def _finding(
    line: TranscriptLine,
    severity: str,
    rule: str,
    detail: str,
) -> TranscriptFinding:
    excerpt = line.text if len(line.text) <= 180 else f"{line.text[:177]}..."
    return TranscriptFinding(
        path=line.path,
        line_no=line.line_no,
        timestamp=line.timestamp,
        severity=severity,
        rule=rule,
        detail=detail,
        excerpt=excerpt,
    )
