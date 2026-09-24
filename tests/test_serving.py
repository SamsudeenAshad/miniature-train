"""Serving + promotion tests (FR-013/FR-016 slice)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_release = _load("release", ROOT / "services/control-api/release.py")
_predict = _load("predict", ROOT / "services/inference/predict.py")
approve, promote, propose, rollback = _release.approve, _release.promote, _release.propose, _release.rollback
predict = _predict.predict

from ml.data_generator import generate_rows
from ml.features import fit_preprocessing
from ml.training import train_and_evaluate


def _model():
    rows = generate_rows(seed=42)
    by_mean = fit_preprocessing(rows)["train_mean"]
    rep = train_and_evaluate(rows, seed=42, train_mean=by_mean)
    return rep["model"]


def test_inference_contract():
    m = _model()
    out = predict(
        {"series_id": "store_1_sku_1", "hour": 9, "day_of_week": 0, "is_weekend": 0, "on_promotion": 0,
         "history": [20] * 200},
        m, request_id="req_test1",
    )
    assert out["request_id"] == "req_test1"
    assert out["prediction"] >= 0
    assert "model_version" in out and "feature_version" in out


def test_inference_rejects_bad_input():
    m = _model()
    with pytest.raises(ValueError):
        predict({"series_id": "x"}, m)
    with pytest.raises(ValueError):
        predict({"series_id": "x", "hour": 1, "day_of_week": 0, "is_weekend": 0, "on_promotion": 0,
                 "history": [1] * 20000}, m)


def test_promotion_lifecycle_and_guards():
    r = propose(2, "digest-b", requester="ml-eng")
    with pytest.raises(ValueError):
        approve(r, approver="ml-eng", gates_pass=True)  # self-approval
    with pytest.raises(ValueError):
        approve(r, approver="owner", gates_pass=False)  # gates
    r = approve(r, approver="owner", gates_pass=True)
    with pytest.raises(ValueError):
        promote(r, previous_digest="digest-a", shadow_ok=False)
    r = promote(r, previous_digest="digest-a", shadow_ok=True)
    assert r["state"] == "promoted"
    r = rollback(r)
    assert r["state"] == "rolled_back"
    assert r["artifact_digest"] == "digest-a"
