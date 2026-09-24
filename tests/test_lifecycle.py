"""Job + incident lifecycle tests (FR-007/026 slice)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


jobs = _load("jobs", "workers/training/jobs.py")
inc = _load("incidents", "services/control-api/incidents.py")


def test_job_retry_cancel_recover():
    idem: dict = {}
    r = jobs.submit("run-1", idem, "k1")
    assert jobs.submit("run-1", idem, "k1") is r
    r = jobs.start_attempt(r, 1)
    r = jobs.recover(r)
    assert r["state"] == "queued" and r["attempts"][-1]["result"] == "crashed"
    r = jobs.start_attempt(r, 2)
    r = jobs.finish(r, "succeeded")
    assert r["state"] == "succeeded"
    with pytest.raises(ValueError):
        jobs.cancel(r)


def test_incident_guards():
    i = inc.create("high", "owner-1")
    with pytest.raises(ValueError):
        inc.transition(i, "acknowledged", "viewer", "looking", 1)
    with pytest.raises(ValueError):
        inc.transition(i, "resolved", "operator", "", 1, evidence=True)
    with pytest.raises(ValueError):
        inc.transition(i, "resolved", "operator", "fixed", 1, evidence=False)
    i = inc.transition(i, "acknowledged", "operator", "looking", 1)
    i = inc.transition(i, "resolved", "operator", "fixed", 2, evidence=True)
    i = inc.transition(i, "closed", "operator", "done", 3)
    assert i["state"] == "closed" and i["version"] == 4
