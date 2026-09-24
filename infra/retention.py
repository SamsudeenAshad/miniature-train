"""Retention + deletion tombstones (FR-036 slice)."""

from __future__ import annotations

RETENTION_DAYS = {"logs": 7, "traces": 3, "metrics": 15, "predictions": 90, "incidents": 180, "audit": 180}

_tombs: set[str] = set()


def reset() -> None:
    _tombs.clear()


def request_delete(obj_id: str, active_refs: set[str], hold: dict | None = None) -> dict:
    if hold and not hold.get("expired", True):
        return {"deleted": False, "reason": "retention_hold"}
    if obj_id in active_refs:
        return {"deleted": False, "reason": "active_reference"}
    _tombs.add(obj_id)
    return {"deleted": True, "tombstone": obj_id}


def after_restore(ids: list[str]) -> dict:
    """Restored backups must not resurrect deleted records."""
    resurrected = [i for i in ids if i in _tombs]
    return {"reapplied": sorted(resurrected)}
