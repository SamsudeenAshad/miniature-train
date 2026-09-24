"""Outbox tests (ADR-02, SRS 10.4 slice)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ob = _load("outbox", "services/control-api/outbox.py")


def test_publish_consume_dedup():
    ob.reset()
    e = ob.publish("anomaly.detected", "p1", {"score": 0.8})
    assert e["schema_version"] == "1.0" and e["event_id"]
    assert ob.consume(e)["deduped"] is False
    assert ob.consume(e)["deduped"] is True
