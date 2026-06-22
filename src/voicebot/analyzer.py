from __future__ import annotations

import json
import re
from pathlib import Path

from .config import Settings


BUG_REPORT_HEADER = """# Bug Report

This report is generated from submitted call transcripts. Review each finding against the MP3 before final submission.
"""


def generate_bug_report(settings: Settings, use_openai: bool = True) -> Path:
    transcripts = sorted(settings.artifacts_dir.joinpath("transcripts").glob("*.txt"))
    output = settings.artifacts_dir / "BUG_REPORT.md"
    if not transcripts:
        output.write_text(
            BUG_REPORT_HEADER
            + "\nNo transcripts found yet. Run `voicebot fetch-artifacts` after live calls.\n",
            encoding="utf-8",
        )
        return output

    if use_openai and settings.openai_api_key:
        try:
            report = _generate_with_openai(settings, transcripts)
        except Exception as exc:  # noqa: BLE001 - artifact generation should fall back cleanly.
            report = _generate_heuristic(transcripts)
            report += f"\n\n_OpenAI analysis failed; heuristic fallback used. Error: {exc}_\n"
    else:
        report = _generate_heuristic(transcripts)

    output.write_text(report, encoding="utf-8")
    return output


def _generate_with_openai(settings: Settings, transcripts: list[Path]) -> str:
    from openai import OpenAI

    packed = []
    for path in transcripts:
        packed.append(f"--- {path.name} ---\n{path.read_text(encoding='utf-8')[:12000]}")
    prompt = f"""You are reviewing voice-agent QA calls.

Find useful bugs or quality issues in these transcripts. Ignore punctuation nitpicks.
For each issue include:
- Bug title
- Severity: Critical, High, Medium, Low
- Call filename and timestamp
- What happened
- Why it matters
- Expected behavior

Return concise Markdown. If a transcript does not show a bug, do not invent one.

{chr(10).join(packed)}
"""
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(model=settings.analysis_model, input=prompt)
    text = getattr(response, "output_text", "") or str(response)
    return BUG_REPORT_HEADER + "\n" + text.strip() + "\n"


def _generate_heuristic(transcripts: list[Path]) -> str:
    findings: list[dict[str, str]] = []
    for path in transcripts:
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        if "sunday" in lowered and re.search(r"scheduled|booked|confirmed", lowered):
            findings.append(
                {
                    "title": "Possible weekend scheduling without office-hours check",
                    "severity": "High",
                    "call": path.name,
                    "details": "Transcript mentions Sunday and a scheduling confirmation. Verify whether the practice is open on weekends.",
                }
            )
        if "chest" in lowered and not re.search(r"911|emergency|urgent|er|emergency room", lowered):
            findings.append(
                {
                    "title": "Possible unsafe urgent-symptom handling",
                    "severity": "Critical",
                    "call": path.name,
                    "details": "Transcript mentions chest symptoms without an obvious emergency escalation phrase.",
                }
            )
        if "guarantee" in lowered and "insurance" in lowered and re.search(r"\byes\b|covered", lowered):
            findings.append(
                {
                    "title": "Possible insurance over-guarantee",
                    "severity": "Medium",
                    "call": path.name,
                    "details": "Transcript asks about insurance guarantee and may imply coverage without verification.",
                }
            )

    if not findings:
        return BUG_REPORT_HEADER + "\nNo heuristic findings. Manually review transcripts and recordings.\n"

    lines = [BUG_REPORT_HEADER]
    for finding in findings:
        lines.append(
            "\n".join(
                [
                    f"## {finding['title']}",
                    f"- Severity: {finding['severity']}",
                    f"- Call: {finding['call']}",
                    f"- Details: {finding['details']}",
                ]
            )
        )
    lines.append("\nRaw heuristic JSON:\n")
    lines.append("```json")
    lines.append(json.dumps(findings, indent=2))
    lines.append("```")
    return "\n\n".join(lines) + "\n"
