"""Observability tests (FR-017/018/019/021 slice)."""

from workers.aiops.drift import drift_report, retraining_eligible
from workers.aiops.telemetry import redact, telemetry_health


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
