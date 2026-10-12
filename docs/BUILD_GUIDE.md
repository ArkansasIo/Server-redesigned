# Build guide

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
nexarack info
python -m unittest discover -s tests -v
python -m pip install -e ".[api]"
uvicorn nexarack.api:app --reload
```
