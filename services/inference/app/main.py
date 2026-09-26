"""Inference HTTP service (FR-016). Pinned fixture model + feature version in every response."""

import importlib.util
from pathlib import Path

from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[3]

app = FastAPI(title="miniature-train inference", version="0.2.0")


@app.exception_handler(RequestValidationError)
def validation_envelope(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={
        "code": "unprocessable",
        "message": "schema or business-rule validation failed",
        "request_id": request.headers.get("x-request-id", ""),
        "retryable": False,
    })


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
_predict_cached = None


def _predict_fn():
    global _predict_cached
    if _predict_cached is None:
        _predict_cached = _load("predict", "services/inference/predict.py").predict
    return _predict_cached


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


@app.get("/health/ready")
def ready():
    loaded = _model is not None
    return {"status": "ready" if loaded else "warming", "model_loaded": loaded}


@app.post("/predict")
def predict(body: PredictIn, x_request_id: str | None = Header(default=None)):
    payload = body.model_dump()
    predict_mod = _load("predict", "services/inference/predict.py")
    try:
        predict_mod.validate_input(payload)
    except ValueError:
        return JSONResponse(status_code=422, content={
            "code": "unprocessable",
            "message": "schema or business-rule validation failed",
            "request_id": x_request_id or "",
            "retryable": False,
        })
    return _predict_fn()(payload, model(), request_id=x_request_id)
