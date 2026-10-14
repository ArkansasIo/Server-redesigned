# Operations runbook

## Local startup

1. Use Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install with `python -m pip install -e ".[api]"`.
4. Run `uvicorn nexarack.api:app --host 127.0.0.1 --port 8000`.
5. Verify `GET /health`, then inspect `/docs`.

## Configuration

- Default profile: `config/rack-profile.json`.
- Optional custom profile: pass `--config path/to/profile.json` to CLI commands.
- Optional SQLite persistence: set `NEXARACK_DATABASE` to a writable database path.
- Optional CORS allowlist: set `NEXARACK_CORS_ORIGINS` to comma-separated exact origins.

## Diagnostics

- `nexarack info`: print inventory.
- `nexarack run --seconds 30 --workload llm-inference --gpus 8`: run a local simulation.
- `python -m unittest discover -s tests -v`: run tests.
- `GET /health`: check service liveness.
- `GET /history`: inspect telemetry history.
- `GET /exports/history.csv`: download recent telemetry.

## Recovery and data

The simulator state is currently process-local and is reset when the process restarts. SQLite persistence stores explicit snapshots and job records but does not restore an active scheduler automatically. Back up the configured SQLite database file using a SQLite-consistent backup process.

## Public deployment warning

This service has mutating routes and is not an authenticated multi-tenant control plane. Keep it on localhost or behind a trusted private network until authentication, authorization, and request rate controls are implemented and tested.
