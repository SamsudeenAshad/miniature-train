"""Inference HTTP service (FR-016). Pinned fixture model + feature version in every response."""

import importlib.util
from pathlib import Path

from fastapi import FastAPI, Header
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[3]

app = FastAPI(title="miniature-train inference", version="0.1.0")


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class PredictIn(BaseModel):
    series_id: str
    hour: int
    day_of_week: int
    is_weekend: int
    on_promotion: int
    history: list[int]


_model = None


def model():
    global _model
    if _model is None:
        from ml.data_generator import generate_rows
        from ml.features import fit_preprocessing
        from ml.training import train_and_evaluate

        rows = generate_rows(seed=42)
        _model = train_and_evaluate(rows, seed=42, train_mean=fit_preprocessing(rows)["train_mean"])["model"]
    return _model


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.post("/predict")
def predict(body: PredictIn, x_request_id: str | None = Header(default=None)):
    predict_fn = _load("predict", "services/inference/predict.py").predict
    return predict_fn(body.model_dump(), model(), request_id=x_request_id)
