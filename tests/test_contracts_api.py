"""API contract tests (FR-038 slice)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c = _load("contracts", "services/control-api/contracts.py")


def test_error_envelope():
    e = c.error(409, "stale version")
    assert e["code"] == "conflict" and e["retryable"] is False
    assert c.error(503, "down")["retryable"] is True
    assert "stack" not in str(e)


def test_idempotency_conflict():
    c.reset()
    r1 = c.submit("k1", {"a": 1})
    r2 = c.submit("k1", {"a": 1})
    assert r1 == r2
    c.attach("k1", "project_id", "proj_1")
    assert c.submit("k1", {"a": 1})["project_id"] == "proj_1"
    with pytest.raises(ValueError, match="409"):
        c.submit("k1", {"a": 2})
