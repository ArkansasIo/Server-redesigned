"""FastAPI application for the NexaRack analytical simulator."""
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

from .config import load_config
from .engine import SimulationEngine
from .exporting import records_to_csv
from .timeline import WorkloadTimeline
from .storage import SimulationStore

VERSION = "0.5.0"
app = FastAPI(
    title="NexaRack API",
    version=VERSION,
    description="Analytical rack-scale AI infrastructure simulator; not physical hardware telemetry.",
)

# Cross-origin access is disabled unless explicit origins are configured.
_origins = [item.strip() for item in os.getenv("NEXARACK_CORS_ORIGINS", "").split(",") if item.strip()]
if _origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

engine = SimulationEngine(load_config())
timeline = WorkloadTimeline()
_store_path = os.getenv("NEXARACK_DATABASE")
store = SimulationStore(_store_path) if _store_path else None


class WorkloadRequest(BaseModel):
    kind: str = Field(default="matrix", description="Workload preset")
    operations_tflop: float | None = Field(default=None, gt=0)
    memory_gib: float | None = Field(default=None, ge=0)
    gpu_count: int = Field(default=8, ge=1, le=72)
    precision: str = Field(default="fp16", pattern="^(fp8|fp16)$")


@app.get("/", response_class=HTMLResponse, tags=["dashboard"])
def dashboard():
    path = Path(__file__).resolve().parents[2] / "dashboard" / "index.html"
    if not path.exists():
        return HTMLResponse("<h1>NexaRack dashboard not found</h1>", status_code=500)
    return HTMLResponse(path.read_text(encoding="utf-8"))


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "simulation_only": True, "version": VERSION, "persistence_enabled": store is not None}


@app.get("/inventory", tags=["simulation"])
def inventory():
    return engine.rack.inventory()


def _empty_metrics():
    return {
        "time_seconds": 0,
        "gpu_count": len(engine.rack.gpus),
        "gpu_utilization_avg": 0,
        "gpus_active": 0,
        "active_gpu_ids": [],
        "queued_jobs": 0,
        "active_jobs": 0,
        "completed_jobs": 0,
        "power": {
            "rack_power_w": sum(g.power_w for g in engine.rack.gpus) + sum(c.power_w for c in engine.rack.cpus),
            "rack_power_limit_w": engine.config["rack"]["power_limit_w"],
            "rack_temperature_c": engine.config["rack"].get("ambient_c", 22),
            "energy_kwh": 0,
        },
    }


@app.get("/metrics", tags=["telemetry"])
def metrics():
    return engine.history[-1] if engine.history else _empty_metrics()


@app.get("/workloads", tags=["workloads"])
def workloads():
    jobs = engine.scheduler.queue + engine.scheduler.active + engine.scheduler.completed
    return {"jobs": [job.to_dict() for job in jobs]}


@app.get("/timeline", tags=["telemetry"])
def events():
    return {"events": timeline.snapshot()}


@app.get("/history", tags=["telemetry"])
def history(limit: int = Query(default=100, ge=1, le=5000)):
    return {"history": engine.history[-limit:]}


@app.post("/workloads", tags=["workloads"])
def submit(request: WorkloadRequest):
    try:
        job = engine.submit(
            request.kind, request.operations_tflop, request.memory_gib,
            request.gpu_count, request.precision,
        )
        timeline.record("queued", job, engine.time_seconds)
        return job.to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/tick", tags=["simulation"])
def tick(seconds: float = Query(default=1.0, gt=0, le=3600)):
    try:
        result = engine.tick(seconds)
        for job in engine.scheduler.active + engine.scheduler.completed:
            timeline.record(job.status, job, engine.time_seconds)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/exports/history.csv", tags=["exports"])
def export_history(limit: int = Query(default=100, ge=1, le=5000)):
    csv_text = records_to_csv(engine.history[-limit:])
    return StreamingResponse(
        iter([csv_text]), media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="nexarack-history.csv"'},
    )


@app.get("/exports/workloads.csv", tags=["exports"])
def export_workloads():
    jobs = engine.scheduler.queue + engine.scheduler.active + engine.scheduler.completed
    csv_text = records_to_csv([job.to_dict() for job in jobs])
    return StreamingResponse(
        iter([csv_text]), media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="nexarack-workloads.csv"'},
    )


@app.post("/snapshots", tags=["storage"])
def save_snapshot():
    if store is None:
        raise HTTPException(status_code=503, detail="Persistence is disabled; set NEXARACK_DATABASE to enable SQLite storage.")
    snapshot = engine.run_snapshot() if hasattr(engine, "run_snapshot") else {
        "inventory": engine.rack.inventory(),
        "simulation_seconds": engine.time_seconds,
        "metrics": metrics(),
        "jobs": workloads()["jobs"],
    }
    snapshot_id = store.save_snapshot(snapshot)
    for job in snapshot["jobs"]:
        store.save_job(job)
    return {"status": "saved", "snapshot_id": snapshot_id, "jobs_saved": len(snapshot["jobs"])}


@app.get("/storage/snapshots", tags=["storage"])
def stored_snapshots(limit: int = Query(default=100, ge=1, le=5000)):
    if store is None:
        raise HTTPException(status_code=503, detail="Persistence is disabled; set NEXARACK_DATABASE to enable SQLite storage.")
    return {"snapshots": store.list_snapshots(limit)}


@app.get("/storage/jobs", tags=["storage"])
def stored_jobs(limit: int = Query(default=500, ge=1, le=5000)):
    if store is None:
        raise HTTPException(status_code=503, detail="Persistence is disabled; set NEXARACK_DATABASE to enable SQLite storage.")
    return {"jobs": store.list_jobs(limit)}


@app.post("/reset", tags=["simulation"])
def reset():
    global engine, timeline
    engine = SimulationEngine(load_config())
    timeline = WorkloadTimeline()
    return {"status": "reset", "persistence_enabled": store is not None}
