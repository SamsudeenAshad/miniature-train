"""Canary guard tests (FR-014, SRS 11.3 slice)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


canary = _load("canary", "services/control-api/canary.py")


def test_interval_guards():
    assert canary.eval_interval(0, 50, 0.001, 100)["verdict"] == "insufficient"
    assert canary.eval_interval(2, 1000, 0.001, 100)["verdict"] == "pass"
    assert canary.eval_interval(20, 1000, 0.001, 100)["verdict"] == "fail"
    assert canary.eval_interval(60, 1000, 0.001, 100)["verdict"] == "abort"
    assert canary.eval_interval(2, 1000, 0.001, 350)["verdict"] == "fail"


def test_stage_advance_and_abort():
    assert canary.advance(5, 6, 1500, 0, 0)["action"] == "promote"
    assert canary.advance(5, 2, 1500, 0, 0)["action"] == "hold"
    assert canary.advance(25, 6, 1500, 3, 0)["action"] == "abort"
    assert canary.advance(50, 6, 1500, 0, 45)["action"] == "review"
    assert canary.advance(100, 11, 5000, 0, 0)["action"] == "observe"
