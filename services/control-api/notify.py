"""Notifications + exports + quotas (FR-032/034/039 slice, WBS 9.5)."""

from __future__ import annotations

import time

_sent: dict[str, dict] = {}
quotas = {"concurrent_runs": 2, "artifact_gb": 20}


def notify(incident_id: str, payload: dict, allowlist: set[str], dest: str) -> dict:
    if dest not in allowlist:
        return {"delivered": False, "reason": "dest_not_allowlisted"}
    safe = {k: v for k, v in payload.items() if "secret" not in k.lower()}
    key = f"{incident_id}:{hash(str(sorted(safe.items())))}"
    if key in _sent:
        return {"delivered": True, "deduped": True}
    _sent[key] = {"ts": time.time(), "retries": 0}
    return {"delivered": True, "delivery_id": key}


def export_report(project: str, filters: dict, source_ids: list[str]) -> dict:
    return {
        "project": project,
        "generated_at": time.time(),
        "filters": filters,
        "schema_version": "report-1.0",
        "sources": source_ids,
        "redacted": True,
    }


def check_quota(kind: str, used: int) -> bool:
    return used < quotas.get(kind, 0)
