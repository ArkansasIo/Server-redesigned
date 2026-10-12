# NexaRack — AI Server Simulation Platform

NexaRack is a modular Python software simulator for rack-scale AI infrastructure inspired by 2025-era Blackwell systems. It models logical compute devices, memory capacity, workloads, interconnect traffic, power, cooling, and metrics. It does not emulate proprietary GPU hardware or claim physical-server performance.

## Project status
Initial repository bootstrap. The complete local project bundle includes the simulator engine, configuration, dashboard, optional REST API, benchmark reporting, examples, docs, and automated tests.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
nexarack info
nexarack run --seconds 30 --workload llm-inference --gpus 8 --output outputs/run.json
python -m unittest discover -s tests -v
```

For the dashboard and REST API, install `python -m pip install -e ".[api]"` and run `uvicorn nexarack.api:app --reload`, then open `http://127.0.0.1:8000`.

See the downloadable project bundle for the full source tree and test suite. Hardware figures are configurable modeling assumptions and must be validated against measured systems.
