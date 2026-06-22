from __future__ import annotations

import time
from pathlib import Path
from uuid import uuid4

import typer
from rich.console import Console
from rich.table import Table

from .analyzer import generate_bug_report
from .artifacts import ArtifactStore
from .config import ConfigError, load_settings, require_live_call_settings
from .scenarios import all_scenarios, get_scenario, scenario_markdown
from .twilio_client import download_recordings, place_assessment_call, wait_for_call_completion
from .twiml import build_twiml

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def doctor() -> None:
    """Check local configuration without placing a call."""
    settings = load_settings()
    table = Table("Check", "Value")
    table.add_row("Target number", settings.target_test_number)
    table.add_row("Public base URL", settings.public_base_url)
    table.add_row("Stream URL", settings.stream_url)
    table.add_row("Artifacts dir", str(settings.artifacts_dir))
    table.add_row("Realtime model", settings.realtime_model)
    table.add_row("Realtime session style", settings.realtime_session_style)
    console.print(table)
    try:
        require_live_call_settings(settings)
    except ConfigError as exc:
        console.print(f"[yellow]Live call settings incomplete: {exc}[/yellow]")
    else:
        console.print("[green]Live call settings are present.[/green]")


@app.command("scenarios")
def list_scenarios() -> None:
    """List the built-in call scenarios."""
    console.print(scenario_markdown())


@app.command()
def twiml(
    scenario_id: str = typer.Argument("appointment-simple"),
    run_id: str = typer.Option("manual", help="Run identifier included in Twilio stream params."),
) -> None:
    """Print TwiML for local inspection."""
    settings = load_settings()
    scenario = get_scenario(scenario_id)
    console.print(build_twiml(settings=settings, scenario=scenario, run_id=run_id))


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host for FastAPI."),
    port: int = typer.Option(8000, help="Port for FastAPI."),
) -> None:
    """Run the Twilio webhook and media WebSocket server."""
    import uvicorn

    from .server import create_app

    settings = load_settings()
    uvicorn.run(create_app(settings), host=host, port=port)


@app.command()
def call(
    scenario_id: str = typer.Argument("appointment-simple"),
    yes: bool = typer.Option(False, "--yes", help="Actually place the live assessment call."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print what would be called."),
    wait: bool = typer.Option(True, "--wait/--no-wait", help="Wait for the call to finish."),
) -> None:
    """Place one assessment call."""
    settings = load_settings()
    scenario = get_scenario(scenario_id)
    store = ArtifactStore(settings.artifacts_dir)
    run_id = uuid4().hex[:10]

    if dry_run or not yes:
        console.print("[yellow]Dry run only. Pass --yes to place a real call.[/yellow]")
        console.print(f"Target: {settings.target_test_number}")
        console.print(f"Scenario: {scenario.id} - {scenario.title}")
        console.print(f"TwiML URL: {settings.twiml_url}?scenario_id={scenario.id}&run_id={run_id}")
        return

    placed = place_assessment_call(settings=settings, scenario=scenario, store=store, run_id=run_id)
    console.print(
        f"[green]Placed call {placed.call_sid}[/green] "
        f"for scenario {placed.scenario_id}; status={placed.status}"
    )
    if wait:
        result = wait_for_call_completion(settings=settings, call_sid=placed.call_sid)
        console.print(
            f"Call finished: status={result['status']} "
            f"duration={result['duration']} error={result['error_code']}"
        )


@app.command("run-suite")
def run_suite(
    count: int = typer.Option(12, help="Number of scenarios to call."),
    start_index: int = typer.Option(1, help="1-based scenario index to start from."),
    spacing_seconds: int | None = typer.Option(None, help="Seconds to wait between calls."),
    yes: bool = typer.Option(False, "--yes", help="Actually place live assessment calls."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print planned calls only."),
) -> None:
    """Run the scenario suite."""
    settings = load_settings()
    store = ArtifactStore(settings.artifacts_dir)
    spacing = spacing_seconds or settings.run_suite_spacing_seconds
    all_defined = list(all_scenarios())
    start = max(start_index - 1, 0)
    scenarios = all_defined[start : start + count]
    if count > len(scenarios):
        console.print(f"[yellow]Only {len(scenarios)} scenarios are available from that start index.[/yellow]")

    for index, scenario in enumerate(scenarios, start=1):
        run_id = f"suite-{index:02d}-{uuid4().hex[:6]}"
        console.print(f"[bold]{index}/{len(scenarios)}[/bold] {scenario.id}: {scenario.title}")
        if dry_run or not yes:
            console.print(
                f"Dry run: would call {settings.target_test_number} with run_id={run_id}"
            )
            continue
        placed = place_assessment_call(
            settings=settings,
            scenario=scenario,
            store=store,
            run_id=run_id,
        )
        console.print(f"Placed {placed.call_sid}; waiting for completion.")
        result = wait_for_call_completion(settings=settings, call_sid=placed.call_sid)
        console.print(
            f"Finished {placed.call_sid}: status={result['status']} "
            f"duration={result['duration']} error={result['error_code']}"
        )
        if index < len(scenarios):
            console.print(f"Waiting {spacing}s before next call.")
            time.sleep(spacing)


@app.command("fetch-artifacts")
def fetch_artifacts(
    recordings: bool = typer.Option(True, help="Download Twilio MP3 recordings."),
    transcripts: bool = typer.Option(True, help="Rebuild transcripts from event logs."),
) -> None:
    """Download recordings and rebuild transcripts after calls."""
    settings = load_settings()
    store = ArtifactStore(settings.artifacts_dir)
    if recordings:
        paths = download_recordings(settings, store)
        console.print(f"Downloaded/found {len(paths)} recording files.")
    if transcripts:
        paths = store.rebuild_transcripts()
        console.print(f"Rebuilt {len(paths)} transcript files.")


@app.command()
def analyze(
    offline: bool = typer.Option(False, help="Use heuristic analysis only."),
) -> None:
    """Generate artifacts/BUG_REPORT.md from transcripts."""
    settings = load_settings()
    output = generate_bug_report(settings, use_openai=not offline)
    console.print(f"Wrote {Path(output)}")
