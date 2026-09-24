"""Versioned features, fitted preprocessing, offline/online parity (FR-006, WBS 3.4).

Fit statistics on training data only. Package fitted params with the model.
Fixed fixture must produce equivalent offline and online outputs within
tolerance. No future values enter features for prediction time t.
"""

from __future__ import annotations

import hashlib
import json

FEATURE_VERSION = "demand-features-1.0"
TOLERANCE = 1e-9
LAG_HOURS = (1, 24, 168)


def fit_preprocessing(train_rows: list[dict]) -> dict:
    """Fit imputer/scaler on training orders only."""
    orders = [int(r["orders"]) for r in train_rows if r["split"] == "train"]
    if not orders:
        raise ValueError("no train rows to fit on")
    mean = sum(orders) / len(orders)
    var = sum((o - mean) ** 2 for o in orders) / len(orders)
    std = var**0.5 or 1.0
    params = {
        "feature_version": FEATURE_VERSION,
        "train_mean": mean,
        "train_std": std,
        "train_count": len(orders),
    }
    params["code_digest"] = hashlib.sha256(
        json.dumps({k: params[k] for k in ("feature_version", "train_mean", "train_std")}, sort_keys=True).encode()
    ).hexdigest()[:16]
    return params


def _history_lookup(index: dict[tuple, int], series: str, ts_order: list, pos: int, lag: int):
    j = pos - lag
    if j < 0:
        return None
    return ts_order[j]


def build_matrix(rows: list[dict], params: dict) -> list[dict]:
    """Offline batch features. Uses only history available at time t."""
    by_series: dict[str, list[dict]] = {}
    for r in sorted(rows, key=lambda x: (x["series_id"], x["event_time"])):
        by_series.setdefault(r["series_id"], []).append(r)
    out: list[dict] = []
    mean, std = params["train_mean"], params["train_std"]
    for sid, seq in by_series.items():
        orders_hist = [int(r["orders"]) for r in seq]
        for pos, r in enumerate(seq):
            feats = {
                "hour": r["hour"] / 23.0,
                "dow": r["day_of_week"] / 6.0,
                "is_weekend": float(r["is_weekend"]),
                "on_promotion": float(r["on_promotion"]),
            }
            for lag in LAG_HOURS:
                v = orders_hist[pos - lag] if pos - lag >= 0 else None
                feats[f"lag_{lag}"] = ((v - mean) / std) if v is not None else 0.0
                feats[f"lag_{lag}_missing"] = 0.0 if v is not None else 1.0
            out.append({"series_id": sid, "event_time": r["event_time"], "features": feats, "orders": int(r["orders"])})
    return out


def online_features(series_history: list[int], current: dict, params: dict) -> dict:
    """Online single-row features. Must match build_matrix for same inputs."""
    mean, std = params["train_mean"], params["train_std"]
    feats = {
        "hour": current["hour"] / 23.0,
        "dow": current["day_of_week"] / 6.0,
        "is_weekend": float(current["is_weekend"]),
        "on_promotion": float(current["on_promotion"]),
    }
    for lag in LAG_HOURS:
        v = series_history[-lag] if len(series_history) >= lag else None
        feats[f"lag_{lag}"] = ((v - mean) / std) if v is not None else 0.0
        feats[f"lag_{lag}_missing"] = 0.0 if v is not None else 1.0
    return feats
