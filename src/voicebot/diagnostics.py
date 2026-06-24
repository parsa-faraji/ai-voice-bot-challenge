from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

import httpx

from .config import Settings
from .scenarios import Scenario


@dataclass(frozen=True)
class DiagnosticCheck:
    name: str
    ok: bool
    detail: str


def validate_public_tunnel(
    settings: Settings,
    scenario: Scenario,
    *,
    client: httpx.Client | None = None,
    timeout_seconds: float = 10.0,
) -> list[DiagnosticCheck]:
    """Check that Twilio can reach the public webhook before a paid call."""
    checks: list[DiagnosticCheck] = []
    parsed = urlparse(settings.public_base_url)
    checks.append(
        DiagnosticCheck(
            name="HTTPS public URL",
            ok=parsed.scheme == "https",
            detail=settings.public_base_url,
        )
    )

    owns_client = client is None
    http_client = client or httpx.Client(timeout=timeout_seconds)
    try:
        checks.extend(_request_checks(settings, scenario, http_client))
    finally:
        if owns_client:
            http_client.close()
    return checks


def _request_checks(
    settings: Settings,
    scenario: Scenario,
    client: httpx.Client,
) -> list[DiagnosticCheck]:
    checks: list[DiagnosticCheck] = []

    health_url = f"{settings.public_base_url.rstrip('/')}/health"
    try:
        health = client.get(health_url)
        health.raise_for_status()
        body = health.json()
        checks.append(
            DiagnosticCheck(
                name="Public /health",
                ok=body == {"status": "ok"},
                detail=f"{health.status_code} {body}",
            )
        )
    except (httpx.HTTPError, ValueError) as exc:
        checks.append(
            DiagnosticCheck(
                name="Public /health",
                ok=False,
                detail=f"{health_url}: {exc}",
            )
        )

    try:
        twiml = client.get(
            settings.twiml_url,
            params={"scenario_id": scenario.id, "run_id": "doctor"},
        )
        twiml.raise_for_status()
        body = twiml.text
        missing = [
            expected
            for expected in (settings.stream_url, scenario.id, "doctor")
            if expected not in body
        ]
        checks.append(
            DiagnosticCheck(
                name="Public /twiml",
                ok=not missing,
                detail=(
                    f"{twiml.status_code}; stream/scenario/run_id present"
                    if not missing
                    else f"{twiml.status_code}; missing {', '.join(missing)}"
                ),
            )
        )
    except httpx.HTTPError as exc:
        checks.append(
            DiagnosticCheck(
                name="Public /twiml",
                ok=False,
                detail=f"{settings.twiml_url}: {exc}",
            )
        )

    return checks
