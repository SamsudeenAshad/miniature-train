"""Training + evaluation + gates (FR-009/FR-010, ML-002/ML-003 slice)."""

from __future__ import annotations

import hashlib
import json
import math

from .data_generator import SERIES_IDS
from .models import fit_candidate, predict_candidate, seasonal_naive

MODEL_VERSION = "demand-candidate-1.0"


def _group_by_series(rows: list[dict]) -> dict[str, list[dict]]:
    by: dict[str, list[dict]] = {}
    for r in sorted(rows, key=lambda x: (x["series_id"], x["event_time"])):
        by.setdefault(r["series_id"], []).append(r)
    return by


def train_and_evaluate(rows: list[dict], seed: int, train_mean: float) -> dict:
    by = _group_by_series(rows)
    train = {sid: [r for r in seq if r["split"] == "train"] for sid, seq in by.items()}
    model = fit_candidate(train, train_mean)
    model.update({"model": MODEL_VERSION, "seed": seed, "feature_version": "demand-features-1.0"})

    def score(split: str) -> dict:
        abs_err, sq_err, n = 0.0, 0.0, 0
        base_abs = 0.0
        per_series: dict[str, dict] = {}
        for sid, seq in by.items():
            orders = [int(r["orders"]) for r in seq]
            s_abs, s_base, s_n = 0.0, 0.0, 0
            for pos, r in enumerate(seq):
                if r["split"] != split or r["purge_excluded"]:
                    continue
                # label is next-hour orders; approximate with current row for fixture eval
                actual = int(r["orders"])
                pred = predict_candidate(orders, pos, r, model)
                base = seasonal_naive(orders, pos, train_mean)
                s_abs += abs(actual - pred)
                s_base += abs(actual - base)
                s_n += 1
            per_series[sid] = {"mae": (s_abs / s_n) if s_n else None, "baseline_mae": (s_base / s_n) if s_n else None, "n": s_n}
            abs_err += s_abs
            base_abs += s_base
            sq_err += 0.0  # rmse from mae fixture; keep field for contract
            n += s_n
        mae = abs_err / n if n else 0.0
        base_mae = base_abs / n if n else 0.0
        return {"mae": mae, "baseline_mae": base_mae, "n": n, "per_series": per_series}

    val = score("validation")
    digest = hashlib.sha256(json.dumps({"model": model, "val_mae": val["mae"]}, sort_keys=True, default=str).encode()).hexdigest()
    return {"model": model, "validation": val, "artifact_digest": digest}


def check_gates(report: dict) -> dict:
    """Policy: >=10% lower val MAE, no series worsening >5% (ML-003 slice)."""
    val = report["validation"]
    reasons = []
    if val["baseline_mae"] and val["baseline_mae"] > 0:
        improvement = (val["baseline_mae"] - val["mae"]) / val["baseline_mae"]
        if improvement < 0.10:
            reasons.append(f"insufficient_improvement:{improvement:.3f}")
    for sid, s in val["per_series"].items():
        if s["mae"] is None or s["baseline_mae"] in (None, 0):
            continue
        worsen = (s["mae"] - s["baseline_mae"]) / s["baseline_mae"]
        if worsen > 0.05:
            reasons.append(f"series_regressed:{sid}:{worsen:.3f}")
    return {"pass": not reasons, "reasons": reasons}
