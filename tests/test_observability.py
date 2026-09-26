"""Observability tests (FR-017/018/019/021 slice)."""

from pathlib import Path

import yaml

from workers.aiops import drift as drift_mod
from workers.aiops.drift import drift_report, retraining_eligible
from workers.aiops.telemetry import redact, telemetry_health

ROOT = Path(__file__).resolve().parents[1]


def test_redaction():
    r = redact({"authorization": "Bearer x", "orders": 5})
    assert r["authorization"] == "[redacted]"
    assert r["orders"] == 5


def test_telemetry_inhibits_on_loss():
    h = telemetry_health([{"window": "w1", "expected": 1000, "received": 900, "late_s": 5, "skew_s": 1}])
    assert h["monitoring_health"] == "degraded"
    assert h["inhibit_actions"] is True
    h2 = telemetry_health([{"window": "w1", "expected": 1000, "received": 1000, "late_s": 5, "skew_s": 1}])
    assert h2["monitoring_health"] == "healthy"


def test_drift_and_proposal_gates():
    stable = drift_report([10.0] * 600, [10.1] * 600, "orders")
    assert stable["status"] == "stable"
    shifted = drift_report([10.0] * 600, [13.0] * 600, "orders")
    assert shifted["status"] == "drift"
    low = drift_report([10.0] * 600, [13.0] * 100, "orders")
    assert low["status"] == "insufficient-data"
    ok = retraining_eligible("drift", joined_labels=600, coverage=0.9, hours_since_last=30)
    assert ok["eligible"] is True and ok["auto_promote"] is False
    cool = retraining_eligible("drift", joined_labels=600, coverage=0.9, hours_since_last=2)
    assert cool["eligible"] is False


def test_drift_bounds_come_from_adapter():
    cfg = yaml.safe_load((ROOT / "workers/aiops/evidently.yaml").read_text())
    assert drift_mod.MIN_OBS == cfg["window"]["min_observations"] == 500
    assert drift_mod.SHIFT_THRESHOLD == cfg["thresholds"]["mean_shift"] == 0.15
