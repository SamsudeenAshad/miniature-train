"""Baselines + candidate (SRS 7.1, ML-003 slice). CPU-only, stdlib.

Baseline: seasonal-naive (orders at t-168) with train-mean fallback.
Candidate: seasonal-naive plus learned per-series promotion lift fitted on
training data only. Deterministic given seed + inputs.
"""

from __future__ import annotations

from ml.data_generator import SERIES_IDS

SEASONAL_LAG = 168


def seasonal_naive(series_orders: list[int], pos: int, train_mean: float) -> float:
    if pos - SEASONAL_LAG >= 0:
        return float(series_orders[pos - SEASONAL_LAG])
    return train_mean


def fit_candidate(train_by_series: dict[str, list[dict]], train_mean: float) -> dict:
    """Learn per-series promo residual over seasonal-naive on train only."""
    lifts: dict[str, float] = {}
    for sid in SERIES_IDS:
        seq = train_by_series.get(sid, [])
        orders = [int(r["orders"]) for r in seq]
        promo_resid, promo_n, plain_resid, plain_n = 0.0, 0, 0.0, 0
        for pos, r in enumerate(seq):
            base = seasonal_naive(orders, pos, train_mean)
            resid = int(r["orders"]) - base
            if int(r["on_promotion"]):
                promo_resid += resid
                promo_n += 1
            else:
                plain_resid += resid
                plain_n += 1
        promo_avg = promo_resid / promo_n if promo_n else 0.0
        plain_avg = plain_resid / plain_n if plain_n else 0.0
        lifts[sid] = promo_avg - plain_avg
    return {"promo_lift": lifts, "train_mean": train_mean}


def predict_candidate(series_orders: list[int], pos: int, row: dict, model: dict) -> float:
    base = seasonal_naive(series_orders, pos, model["train_mean"])
    if int(row["on_promotion"]):
        base += model["promo_lift"].get(row["series_id"], 0.0)
    return max(0.0, base)
