"""Deterministic anomaly baseline + detector contract (FR-022 slice, SRS 7.5).

Per-service robust z-score over 60s windows. ML event after 2 of 3
eligible windows exceed threshold. Scores are normalized anomaly scores,
not calibrated probabilities.
"""

from __future__ import annotations

DETECTOR_VERSION = "stat-baseline-1.0"


def window_score(value: float, ref_mean: float, ref_std: float) -> float:
    std = ref_std or 1.0
    return abs(value - ref_mean) / (3.0 * std)


def detect(windows: list[dict], threshold: float = 0.72) -> dict:
    """windows: [{service, value, ref_mean, ref_std}]. 2-of-3 persistence."""
    hits = [window_score(w["value"], w["ref_mean"], w["ref_std"]) for w in windows[-3:]]
    over = sum(1 for s in hits if s >= threshold)
    triggered = over >= 2 and len(hits) == 3
    score = max(hits) if hits else 0.0
    return {
        "detector_version": DETECTOR_VERSION,
        "score": score,
        "threshold": threshold,
        "triggered": triggered,
        "score_semantics": "normalized_anomaly_score_not_probability",
    }
