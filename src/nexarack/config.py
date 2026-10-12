import json
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "rack-profile.json"

def load_config(path=None):
    with (Path(path) if path else DEFAULT_CONFIG).open(encoding="utf-8") as f:
        cfg = json.load(f)
    for section in ("system", "topology", "gpu", "cpu", "rack", "scheduler"):
        if section not in cfg: raise ValueError(f"Missing config section: {section}")
    for key in ("trays", "gpus_per_tray", "cpus"):
        if int(cfg["topology"].get(key, 0)) < 1: raise ValueError(f"topology.{key} must be >= 1")
    if not 0 < float(cfg["scheduler"].get("compute_efficiency", .35)) <= 1: raise ValueError("compute_efficiency must be in (0, 1]")
    return cfg
