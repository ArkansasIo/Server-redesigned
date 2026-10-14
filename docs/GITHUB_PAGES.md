# GitHub Pages deployment

NexaRack's Python simulator and FastAPI service require a Python runtime; GitHub Pages only serves static files. This repository now includes a separate static demo under `site/` that can be deployed to Pages without pretending to execute the simulation backend.

## Enable Pages

1. Open **Settings → Pages** in the repository.
2. Under **Build and deployment**, select **GitHub Actions** as the source.
3. Push to `main` or run the **Deploy static demo to GitHub Pages** workflow manually.
4. When the workflow finishes, open the Pages URL shown in the deployment job.

## Static demo vs live API

The static site includes a client-side demo model for exploring the console, queueing example jobs, and advancing demo time. It does not call the Python engine and its numbers are illustrative. To use the real simulator, install the project with `python -m pip install -e ".[api]"` and run `uvicorn nexarack.api:app --host 127.0.0.1 --port 8000` locally. For a remotely accessible live API, deploy the Python service to a server platform and configure an API URL plus appropriate CORS and authentication controls; do not expose an unauthenticated simulation/admin endpoint to the public internet.

## Troubleshooting

- **404:** confirm Pages uses the GitHub Actions source and the latest deployment succeeded.
- **Workflow not running:** check Actions are enabled for the repository and inspect the workflow run.
- **Blank page:** open browser developer tools and inspect the console; the static build is just HTML/CSS/JavaScript and requires no npm install.
