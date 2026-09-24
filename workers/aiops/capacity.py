"""Capacity adviser (FR-031 slice, WBS 7.2). Bounded, no auto-execute."""

from __future__ import annotations


def recommend(history: list[float], current_replicas: int, max_replicas: int, unit_cost: float = 0.0) -> dict:
    if len(history) < 24:
        return {"status": "insufficient-data", "recommendation": None}
    # seasonal-naive: same hour last day
    naive = history[-24]
    last = history[-1]
    headroom = 0.3
    target = naive * (1 + headroom)
    want = current_replicas
    if last > naive * 1.2 and current_replicas < max_replicas:
        want = min(max_replicas, current_replicas + 1)
    elif last < naive * 0.7 and current_replicas > 1:
        want = current_replicas - 1
    return {
        "status": "ok",
        "recommendation": {"replicas": want, "max": max_replicas},
        "basis": {"naive": naive, "last": last},
        "uncertainty": "point_estimate_only",
        "assumed_unit_cost": unit_cost,
        "auto_applied": False,
    }
