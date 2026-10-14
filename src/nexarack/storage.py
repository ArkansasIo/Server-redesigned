"""Small SQLite persistence layer for simulation snapshots and job records."""
import json
import sqlite3
from pathlib import Path
from typing import Any


class SimulationStore:
    """Persist snapshots/jobs without coupling the engine to a database."""

    def __init__(self, path: str | Path = "outputs/nexarack.sqlite3"):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    simulation_seconds REAL NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    payload TEXT NOT NULL
                );
            """)

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def save_snapshot(self, snapshot: dict[str, Any]) -> int:
        metrics = snapshot.get("metrics", {})
        with self._connect() as db:
            cur = db.execute(
                "INSERT INTO snapshots(simulation_seconds,payload) VALUES (?,?)",
                (float(snapshot.get("simulation_seconds", metrics.get("time_seconds", 0))),
                 json.dumps(snapshot, separators=(",", ":"))),
            )
            return int(cur.lastrowid)

    def save_job(self, job: dict[str, Any]) -> None:
        with self._connect() as db:
            db.execute("""
                INSERT INTO jobs(job_id,status,payload) VALUES (?,?,?)
                ON CONFLICT(job_id) DO UPDATE SET
                  status=excluded.status, updated_at=CURRENT_TIMESTAMP,
                  payload=excluded.payload
            """, (str(job["id"]), str(job.get("status", "unknown")),
                  json.dumps(job, separators=(",", ":"))))

    def list_snapshots(self, limit: int = 100) -> list[dict[str, Any]]:
        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        with self._connect() as db:
            rows = db.execute(
                "SELECT id,created_at,simulation_seconds,payload FROM snapshots ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [{"id": row["id"], "created_at": row["created_at"],
                 "simulation_seconds": row["simulation_seconds"],
                 "snapshot": json.loads(row["payload"])} for row in reversed(rows)]

    def list_jobs(self, limit: int = 500) -> list[dict[str, Any]]:
        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        with self._connect() as db:
            rows = db.execute(
                "SELECT payload FROM jobs ORDER BY updated_at DESC, job_id LIMIT ?",
                (limit,),
            ).fetchall()
        return [json.loads(row["payload"]) for row in rows]
