# Architecture

NexaRack is an analytical simulator for logical rack-scale compute infrastructure. It does not emulate proprietary hardware, run GPU kernels, or report real physical-server telemetry.

## Runtime modules

- `config.py`: load and validate the JSON rack profile.
- `models.py`: slotted CPU, GPU, and workload data models.
- `inventory.py`: create logical rack inventory.
- `workloads.py`: workload presets and compute/memory/interconnect runtime estimates.
- `scheduler.py`: FIFO GPU placement, memory reservation, job completion, and resource release.
- `interconnect.py`: shared fabric transfer estimates.
- `power.py`: utilization-based power and first-order thermal estimates.
- `engine.py`: simulation clock and telemetry aggregation.
- `timeline.py`: job lifecycle event history.
- `benchmarks.py`: prediction-versus-measurement error summaries.
- `reporting.py` and `exporting.py`: JSON and CSV reports.
- `storage.py`: opt-in SQLite persistence for explicit snapshots and job records.
- `api.py`: optional FastAPI REST interface and browser dashboard.
- `dashboard/index.html`: local dashboard backed by the API.
- `site/index.html`: static GitHub Pages demo, not connected to the Python engine.

## Data flow

```text
CLI / REST API
    |
    v
SimulationEngine -----> WorkloadTimeline
    |                         |
    v                         v
Scheduler <------------ workload events
    |
    +---- Rack inventory
    +---- Interconnect model
    +---- Power / thermal model
    |
    v
Telemetry history -----> JSON / CSV exports
    |
    +---- optional SQLite snapshots and job records
```

## Persistence boundaries

The scheduler and active simulation state remain process-local. SQLite persistence is opt-in through `NEXARACK_DATABASE`; API snapshot requests persist a point-in-time view and current job records. Restart recovery and deterministic replay are not implemented.

## Security boundaries

The API is intended for local or trusted-network development. CORS is disabled by default and can be enabled with an explicit `NEXARACK_CORS_ORIGINS` allowlist. CORS is not authentication. Public multi-tenant deployment requires authentication, authorization, rate limiting, and further operational hardening.
