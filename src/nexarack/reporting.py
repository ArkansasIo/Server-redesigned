import json
from pathlib import Path
def write_json(data,path):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,indent=2),encoding='utf-8'); return p
