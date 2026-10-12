from pathlib import Path
from fastapi.responses import HTMLResponse
DASHBOARD_PATH=Path(__file__).resolve().parents[2]/'dashboard'/'index.html'
def dashboard_response():
    if not DASHBOARD_PATH.exists(): return HTMLResponse('<h1>NexaRack dashboard missing</h1>',status_code=500)
    return HTMLResponse(DASHBOARD_PATH.read_text(encoding='utf-8'))
