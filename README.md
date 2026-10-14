# NexaRack — AI Server Simulation Platform

NexaRack is a configurable Python simulator for rack-scale AI infrastructure inspired by Blackwell-era systems. It models logical GPU/CPU inventory, memory, synthetic workloads, shared interconnect traffic, power, thermal response, metrics, and benchmark error reports. It does not emulate proprietary hardware or claim physical-server performance.

## Quick start

Python 3.11+

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
nexarack info
nexarack run --seconds 30 --workload llm-inference --gpus 8 --output outputs/run.json
python -m unittest discover -s tests -v
```

## Live API and dashboard

```bash
python -m pip install -e ".[api]"
uvicorn nexarack.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`; interactive API documentation is at `/docs`.

## Features

- Configurable rack profile and logical CPU/GPU inventory.
- Synthetic matrix, LLM inference, distributed training, and memory-bandwidth workloads.
- FIFO GPU scheduling, memory reservations, estimated completion, and resource release.
- Compute, memory, interconnect, power, and first-order thermal estimates.
- In-memory telemetry history and workload lifecycle timeline.
- JSON benchmark reports and CSV exports for telemetry and jobs.
- Optional SQLite persistence for explicit snapshots and job records.
- FastAPI REST endpoints and a local operator dashboard.
- Static GitHub Pages demo with browser-side illustrative workloads.
- Unit tests and Python CI workflow.

## GitHub Pages demo

The `site/` folder is a standalone static demo deployable through GitHub Actions. In repository **Settings → Pages**, select **GitHub Actions** as the source. Then run the **Deploy static demo to GitHub Pages** workflow or push changes to `site/`. See [the Pages deployment guide](docs/GITHUB_PAGES.md).

The Pages demo does not run the Python backend; its figures are illustrative and run entirely in the browser.

## Optional SQLite persistence

Set `NEXARACK_DATABASE` to a writable SQLite file path before starting the API. Use `POST /snapshots` to save the current simulator snapshot and job records. Persisted data is not automatically replayed into a restarted simulation.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [REST API reference](docs/API_REFERENCE.md)
- [Build guide](docs/BUILD_GUIDE.md)
- [Operations runbook](docs/OPERATIONS_RUNBOOK.md)
- [GitHub Pages deployment](docs/GITHUB_PAGES.md)
- [Performance assumptions](docs/PERFORMANCE.md)
- [Calibration](docs/CALIBRATION.md)
- [Validation](docs/VALIDATION.md)

## Security and modeling limits

The API is designed for local or trusted-network development. CORS is disabled by default; setting `NEXARACK_CORS_ORIGINS` enables only the listed origins, but CORS is not authentication. Do not expose mutation routes publicly without authentication, authorization, and rate limiting.

Throughput, power, network, and cooling values are configurable analytical assumptions. This is not a cycle-accurate emulator. Validate against measured hardware before using results for engineering, procurement, or operational decisions.
