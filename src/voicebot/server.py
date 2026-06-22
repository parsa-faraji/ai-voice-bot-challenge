from __future__ import annotations

from fastapi import FastAPI, Query, Request, WebSocket
from fastapi.responses import JSONResponse, Response

from .artifacts import ArtifactStore
from .bridge import MediaBridge
from .config import Settings, load_settings
from .scenarios import get_scenario
from .twiml import build_twiml


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or load_settings()
    store = ArtifactStore(settings.artifacts_dir)
    bridge = MediaBridge(settings, store)
    app = FastAPI(title="Athena Assessment Voice Bot")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.api_route("/twiml", methods=["GET", "POST"])
    async def twiml(
        scenario_id: str = Query(default="appointment-simple"),
        run_id: str = Query(default="manual"),
    ) -> Response:
        scenario = get_scenario(scenario_id)
        return Response(
            content=build_twiml(settings=settings, scenario=scenario, run_id=run_id),
            media_type="application/xml",
        )

    @app.post("/stream-status")
    async def stream_status(request: Request) -> JSONResponse:
        form = await request.form()
        store.record_event(
            run_id=str(form.get("run_id") or "stream-status"),
            call_sid=str(form.get("CallSid") or "unknown-call"),
            elapsed_seconds=0.0,
            direction="twilio_status",
            event=dict(form),
        )
        return JSONResponse({"ok": True})

    @app.websocket("/media")
    async def media(websocket: WebSocket) -> None:
        await bridge.run(websocket)

    return app


app = create_app()
