from google.cloud import bigquery
from datetime import datetime, timezone
import json

def _safe_get(d: dict, path: list[str], default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur

def insert_raw_event(project_id: str, dataset: str, table: str, event: dict) -> None:
    client = bigquery.Client(project=project_id)
    table_id = f"{project_id}.{dataset}.{table}"

    # Ajusta estas rutas según el payload real (las dejamos “best effort”)
    submission_id = (
        _safe_get(event, ["data", "submission", "id"])
        or _safe_get(event, ["data", "id"])
        or _safe_get(event, ["submission", "id"])
    )
    form_id = (
        _safe_get(event, ["data", "submission", "form", "id"])
        or _safe_get(event, ["data", "form", "id"])
        or _safe_get(event, ["form", "id"])
    )
    submitted_at = (
        _safe_get(event, ["data", "submission", "submittedAt"])
        or _safe_get(event, ["data", "submittedAt"])
        or _safe_get(event, ["submittedAt"])
    )

    row = {
        "event_type": event.get("type"),
        "submission_id": submission_id,
        "form_id": form_id,
        "submitted_at": submitted_at,   # si viene ISO string, BQ lo parsea si el schema es TIMESTAMP
        "payload": json.dumps(event, ensure_ascii=False),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }

    errors = client.insert_rows_json(table_id, [row])
    if errors:
        raise RuntimeError(f"BigQuery insert_rows_json returned errors: {errors}")
