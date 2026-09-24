"""Feature parity tests (FR-006)."""

from ml.data_generator import generate_rows
from ml.features import TOLERANCE, build_matrix, fit_preprocessing, online_features


def test_fit_uses_train_only():
    rows = generate_rows(seed=42)
    p = fit_preprocessing(rows)
    assert p["train_count"] == 10 * 8 * 7 * 24
    assert p["feature_version"].startswith("demand-features-")


def test_offline_online_parity():
    rows = generate_rows(seed=42)
    params = fit_preprocessing(rows)
    matrix = build_matrix(rows[:2000], params)
    # pick a row with full history: find series with pos >= 168
    target = None
    for m in matrix:
        if m["event_time"] >= "2026-01-12T00:00:00Z":
            target = m
            break
    assert target is not None
    sid = target["series_id"]
    seq = [r for r in sorted(rows, key=lambda x: (x["series_id"], x["event_time"])) if r["series_id"] == sid]
    pos = next(i for i, r in enumerate(seq) if r["event_time"] == target["event_time"])
    hist = [int(r["orders"]) for r in seq[:pos]]
    cur = seq[pos]
    online = online_features(hist, cur, params)
    for k, v in target["features"].items():
        assert abs(online[k] - v) <= TOLERANCE, k


def test_missing_history_imputed_as_zero():
    rows = generate_rows(seed=42)
    params = fit_preprocessing(rows)
    first = sorted([r for r in rows if r["series_id"] == "store_1_sku_1"], key=lambda x: x["event_time"])[0]
    online = online_features([], first, params)
    assert online["lag_1_missing"] == 1.0
    assert online["lag_1"] == 0.0
