"""Inference HTTP tests (Step 52, FR-016 slice)."""

import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("infer_main", str(ROOT / "services/inference/app/main.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_predict_contract_over_http():
    m = _load()
    c = TestClient(m.app)
    r = c.post("/predict", json={"series_id": "store_1_sku_1", "hour": 9, "day_of_week": 0,
                                 "is_weekend": 0, "on_promotion": 0, "history": [20] * 200},
               headers={"x-request-id": "req_http_1"})
    assert r.status_code == 200
    body = r.json()
    assert body["request_id"] == "req_http_1"
    assert body["prediction"] >= 0
    assert "model_version" in body and "feature_version" in body
    anon = c.post("/predict", json={"series_id": "store_1_sku_1", "hour": 9, "day_of_week": 0,
                                    "is_weekend": 0, "on_promotion": 0, "history": [20] * 200})
    assert anon.json()["request_id"].startswith("req_")
    assert c.post("/predict", json={"series_id": "x"}).status_code == 422
    bad = c.post("/predict", json={"series_id": "x"})
    assert bad.json()["code"] == "unprocessable"


def test_readiness_reflects_model():
    m = _load()
    m._model = None
    c = TestClient(m.app)
    assert c.get("/health/ready").json()["status"] == "warming"


def test_predict_fn_cached():
    m = _load()
    assert m._predict_fn() is m._predict_fn()
