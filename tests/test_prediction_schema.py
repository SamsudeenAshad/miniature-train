"""Prediction schema tests (Step 196, FR-016 slice)."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_prediction_conforms():
    schema = json.loads((ROOT / "packages/contracts/schemas/prediction.schema.json").read_text())
    predict = _load("predict", "services/inference/predict.py").predict
    from ml.data_generator import generate_rows
    from ml.features import fit_preprocessing
    from ml.training import train_and_evaluate

    rows = generate_rows(seed=42)
    model = train_and_evaluate(rows, seed=42, train_mean=fit_preprocessing(rows)["train_mean"])["model"]
    out = predict({"series_id": "s", "hour": 1, "day_of_week": 0, "is_weekend": 0,
                   "on_promotion": 0, "history": [5] * 200}, model, request_id="r1")
    for key in schema["required"]:
        assert key in out, key
    assert out["prediction"] >= schema["properties"]["prediction"]["minimum"]
