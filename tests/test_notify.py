"""Notify/export/quota tests (FR-032/034/039 slice)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


n = _load("notify", "services/control-api/notify.py")


def test_webhook_allowlist_and_dedup():
    r1 = n.notify("inc1", {"msg": "hi", "secret_token": "x"}, {"hooks.example"}, "hooks.example")
    assert r1["delivered"] is True
    r2 = n.notify("inc1", {"msg": "hi", "secret_token": "y"}, {"hooks.example"}, "hooks.example")
    assert r2.get("deduped") is True
    bad = n.notify("inc1", {"msg": "hi"}, {"hooks.example"}, "evil.example")
    assert bad["delivered"] is False


def test_export_and_quota():
    rep = n.export_report("p1", {"env": "staging"}, ["run-1"])
    assert rep["redacted"] is True and rep["schema_version"] == "report-1.0"
    assert n.check_quota("concurrent_runs", 1) is True
    assert n.check_quota("concurrent_runs", 5) is False
