# NexaRack — AI Server Simulation Platform

NexaRack is a configurable Python simulator for rack-scale AI infrastructure inspired by 2025-era Blackwell systems. It models logical GPU/CPU inventory, memory, synthetic workloads, shared interconnect traffic, power, thermal response, metrics, and benchmark error reports. It does not emulate proprietary hardware or claim physical-server performance.

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

Optional live dashboard/API:

```bash
python -m pip install -e ".[api]"
uvicorn nexarack.api:app --reload
```

Open `http://127.0.0.1:8000`.

## Browser demo on GitHub Pages

A separate static console is available in [`site/`](site/). To publish it:

1. Open **Settings → Pages**.
2. Set the source to **GitHub Actions**.
3. Push a change to `site/` on `main`, or manually run **Deploy static demo to GitHub Pages** from the Actions tab.
4. Open the Pages URL from the successful deployment.

The static demo is client-side only and uses illustrative values; it does not run the Python simulator. See [GitHub Pages deployment notes](docs/GITHUB_PAGES.md).

## Important limits

All throughput, power, network and cooling values are configurable analytical assumptions. This is not a cycle-accurate emulator. Validate against measured hardware before using results for engineering or purchasing decisions.
