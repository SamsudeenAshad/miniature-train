"""Telemetry health + redaction (FR-020/021 slice, WBS 6.1-6.3)."""

from __future__ import annotations

SENSITIVE = ("authorization", "cookie", "token", "secret", "password")


def redact(record: dict) -> dict:
    return {k: ("[redacted]" if any(s in k.lower() for s in SENSITIVE) else v) for k, v in record.items()}


def telemetry_health(windows: list[dict]) -> dict:
    """windows: [{window, expected, received, late_s, skew_s}]."""
    missing = sum(max(0, w["expected"] - w["received"]) for w in windows)
    total = sum(w["expected"] for w in windows) or 1
    max_skew = max([abs(w.get("skew_s", 0)) for w in windows] or [0])
    stale = any(w.get("late_s", 0) > 30 for w in windows)
    loss_rate = missing / total
    degraded = loss_rate > 0.001 or stale or max_skew > 5
    return {
        "missing": missing,
        "loss_rate": loss_rate,
        "max_skew_s": max_skew,
        "monitoring_health": "degraded" if degraded else "healthy",
        "inhibit_actions": degraded,
    }
