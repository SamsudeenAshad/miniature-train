"""Abort/reconcile tests (FR-015, NFR-006 slice)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ro = _load("rollout", "services/control-api/rollout.py")


def test_abort_enrollment():
    r = {"id": "ro-1"}
    assert ro.request_abort(r, True, False)["action"] == "escalate"
    assert ro.request_abort(r, False, True)["action"] == "hold"
    assert ro.request_abort(r, True, True)["action"] == "abort"


def test_restore_guards():
    r = {"schema": "v1"}
    assert ro.restore_known_good(r, None)["state"] == "escalated"
    assert ro.restore_known_good(r, {"digest": "d", "schema": "v2"})["state"] == "blocked"
    assert ro.restore_known_good(r, {"digest": "d", "schema": "v1"})["state"] == "restoring"


def test_reconcile():
    assert ro.reconcile("a", "a", "stable", "stable", "m1", "m1")["state"] == "verified"
    assert ro.reconcile("b", "a", "stable", "stable", "m1", "m1")["state"] == "reconciliation_required"
