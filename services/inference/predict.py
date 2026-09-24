"""Schema-validated inference (FR-016 slice). No fabricated predictions."""

from __future__ import annotations

import uuid

from ml.features import FEATURE_VERSION
from ml.training import MODEL_VERSION

MAX_BYTES = 10 * 1024
REQUIRED_FIELDS = ("series_id", "hour", "day_of_week", "is_weekend", "on_promotion", "history")


def validate_input(payload: dict) -> None:
    if len(str(payload).encode()) > MAX_BYTES:
        raise ValueError("payload_too_large")
    for f in REQUIRED_FIELDS:
        if f not in payload:
            raise ValueError(f"missing_field:{f}")
    if not isinstance(payload["history"], list):
        raise ValueError("history_must_be_list")


def predict(payload: dict, model: dict, request_id: str | None = None) -> dict:
    validate_input(payload)
    from ml.models import predict_candidate

    hist = [int(x) for x in payload["history"]]
    pos = len(hist)
    row = {"series_id": payload["series_id"], "on_promotion": int(payload["on_promotion"])}
    value = predict_candidate(hist, pos, row, model)
    return {
        "request_id": request_id or f"req_{uuid.uuid4().hex[:12]}",
        "prediction": value,
        "model_version": model.get("model", MODEL_VERSION),
        "feature_version": FEATURE_VERSION,
    }
