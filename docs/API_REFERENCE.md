# NexaRack REST API reference

Run the optional service with:

```bash
python -m pip install -e ".[api]"
uvicorn nexarack.api:app --host 127.0.0.1 --port 8000
```

Interactive OpenAPI docs are served at `/docs`; the schema is available at `/openapi.json`.

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Operator dashboard |
| GET | `/health` | Service liveness and version |
| GET | `/inventory` | Logical CPU/GPU rack inventory |
| GET | `/metrics` | Latest telemetry or initial metrics |
| GET | `/history?limit=100` | In-memory telemetry history |
| GET | `/workloads` | Queued, active and completed jobs |
| GET | `/timeline` | Lifecycle events |
| GET | `/exports/history.csv?limit=100` | Download telemetry history as CSV |
| GET | `/exports/workloads.csv` | Download visible workload records as CSV |
| GET | `/storage/snapshots?limit=100` | Persisted snapshots, when storage is enabled |
| GET | `/storage/jobs?limit=500` | Persisted job records, when storage is enabled |
| POST | `/workloads` | Submit a workload |
| POST | `/tick?seconds=1` | Advance the simulation clock |
| POST | `/snapshots` | Save a snapshot to SQLite |
| POST | `/reset` | Reset in-memory simulation state |

## Workload request

```json
{
  "kind": "llm-inference",
  "operations_tflop": 250,
  "memory_gib": 48,
  "gpu_count": 8,
  "precision": "fp16"
}
```

Supported workload kinds: `matrix`, `llm-inference`, `distributed-training`, and `memory-bandwidth`. Precision is `fp8` or `fp16`. Numeric limits are validated by the API model and simulator.

## Persistence

Set `NEXARACK_DATABASE` to a SQLite file path to enable optional persistence. If it is unset, the API does not create a database automatically. Snapshots and job rows are stored only when the corresponding routes are used. The simulation engine remains in-memory; persisted snapshots are an audit/export history, not automatic crash recovery or replay.

## Security

The API is intended for local development by default. Do not expose mutation routes on a public interface without authentication, authorization, rate limiting, and a deliberate CORS policy. Configure `NEXARACK_CORS_ORIGINS` as a comma-separated allowlist only when cross-origin browser access is required. Never put API secrets in the static GitHub Pages site.
