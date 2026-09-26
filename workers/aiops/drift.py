"""Drift + labels + retraining proposals (FR-017/018/019, ML-006 slice)."""

from __future__ import annotations

from pathlib import Path

import yaml

_ADAPTER = yaml.safe_load((Path(__file__).resolve().parent / "evidently.yaml").read_text())

MIN_OBS = int(_ADAPTER["window"]["min_observations"])
SHIFT_THRESHOLD = float(_ADAPTER["thresholds"]["mean_shift"])
MIN_LABEL_COVERAGE = 0.8
COOLDOWN_H = 24


def drift_report(reference: list[float], current: list[float], name: str) -> dict:
    if len(current) < MIN_OBS:
        return {"metric": name, "status": "insufficient-data", "n": len(current)}
    ref_mean = sum(reference) / len(reference)
    cur_mean = sum(current) / len(current)
    shift = abs(cur_mean - ref_mean) / (abs(ref_mean) or 1.0)
    return {
        "metric": name,
        "status": "drift" if shift > SHIFT_THRESHOLD else "stable",
        "reference_n": len(reference),
        "window_n": len(current),
        "shift": shift,
        "method": f"mean_shift_{SHIFT_THRESHOLD}",
    }


def retraining_eligible(drift_status: str, joined_labels: int, coverage: float, hours_since_last: float) -> dict:
    reasons = []
    if drift_status not in ("drift", "quality_drop"):
        reasons.append("no_trigger")
    if joined_labels < MIN_OBS:
        reasons.append("insufficient_labels")
    if coverage < MIN_LABEL_COVERAGE:
        reasons.append("low_coverage")
    if hours_since_last < COOLDOWN_H:
        reasons.append("cooldown")
    return {"eligible": not reasons, "reasons": reasons, "auto_promote": False}
