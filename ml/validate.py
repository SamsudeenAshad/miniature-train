"""Dataset contract validation (SRS FR-004, WBS 3.3).

Quarantines snapshots with invalid schema, duplicate business keys,
invalid timestamps, missing labels, or failed rules. Emits a
machine-readable report. Pure stdlib.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime

REQUIRED_COLUMNS = [
    "series_id",
    "event_time",
    "orders",
    "promotion_known_at",
    "hour",
    "day_of_week",
    "is_weekend",
    "on_promotion",
    "split",
    "purge_excluded",
]
SCHEMA_VERSION = "demand-schema-1.0"


def _parse_ts(v: str) -> datetime | None:
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except Exception:
        return None


def validate_rows(rows: list[dict]) -> dict:
    findings: list[dict] = []
    seen: set[tuple] = set()
    for i, r in enumerate(rows):
        # schema presence
        for col in REQUIRED_COLUMNS:
            if col not in r or r[col] in (None, ""):
                findings.append({"row": i, "rule": "missing_column", "column": col})
        # business-key uniqueness (series_id, event_time)
        key = (r.get("series_id"), r.get("event_time"))
        if key in seen:
            findings.append({"row": i, "rule": "duplicate_key", "key": list(key)})
        seen.add(key)
        # timestamp validity + ordering (promotion known before event)
        ts = _parse_ts(str(r.get("event_time", "")))
        pk = _parse_ts(str(r.get("promotion_known_at", "")))
        if ts is None:
            findings.append({"row": i, "rule": "invalid_event_time"})
        if pk is None:
            findings.append({"row": i, "rule": "invalid_promotion_known_at"})
        if ts is not None and pk is not None and pk > ts:
            findings.append({"row": i, "rule": "future_leak", "detail": "promotion_known_at after event_time"})
        # ranges
        try:
            orders = int(r.get("orders", -1))
            if orders < 0 or orders > 10000:
                findings.append({"row": i, "rule": "orders_out_of_range"})
        except Exception:
            findings.append({"row": i, "rule": "orders_not_integer"})
        # split label availability
        if r.get("split") not in ("train", "validation", "test"):
            findings.append({"row": i, "rule": "invalid_split"})
    status = "accepted" if not findings else "quarantined"
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True, default=str).encode()).hexdigest()
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "rows": len(rows),
        "finding_count": len(findings),
        "findings": findings[:50],
        "truncated": len(findings) > 50,
        "content_digest": digest,
    }
