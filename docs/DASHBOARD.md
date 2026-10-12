# Dashboard

The bundled responsive dashboard is served at `/` by the optional FastAPI app. It shows inventory, utilization, power, estimated temperature, job state, and workload submission. Start with `pip install -e ".[api]"` and `uvicorn nexarack.api:app --reload`, then open `http://127.0.0.1:8000`.

The dashboard requires the API extra. Keep the development API on localhost; add authentication, authorization, rate limits and deployment hardening before exposing it to a network.
