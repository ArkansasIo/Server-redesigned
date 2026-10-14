"""CSV export helpers for simulator telemetry and workload records."""
import csv
import io
import json
from typing import Any


def records_to_csv(records: list[dict[str, Any]]) -> str:
    """Serialize flat records as CSV; nested values are JSON-encoded."""
    if not records:
        return ""
    columns = list(dict.fromkeys(key for record in records for key in record))
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for record in records:
        writer.writerow({
            key: json.dumps(value, separators=(",", ":")) if isinstance(value, (dict, list))
            else value
            for key, value in record.items()
        })
    return output.getvalue()
