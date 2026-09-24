"""API error + idempotency contract (FR-038 slice)."""

from __future__ import annotations

import hashlib
import json
import uuid

ERRORS = {
    400: "bad_request", 401: "unauthenticated", 403: "forbidden", 404: "not_found",
    409: "conflict", 413: "too_large", 422: "unprocessable", 429: "rate_limited", 503: "unavailable",
}

_store: dict[str, dict] = {}


def reset() -> None:
    _store.clear()


def error(status: int, message: str) -> dict:
    return {
        "code": ERRORS.get(status, "error"),
        "message": message,
        "request_id": f"req_{uuid.uuid4().hex[:12]}",
        "retryable": status in (429, 503),
        "status": status,
    }


def submit(key: str, payload: dict) -> dict:
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
    if key in _store:
        if _store[key]["digest"] != digest:
            raise ValueError("idempotency_conflict_409")
        return _store[key]["response"]
    resp = {"accepted": True, "key": key, "digest": digest}
    _store[key] = {"digest": digest, "response": resp}
    return resp
