"""Watchdog + perf report tests (FR-037, AT-21/22 slice)."""

import pytest

from infra.health import perf_report, watchdog


def test_degraded_rules():
    ok = watchdog(True, True, True, True)
    assert ok["degraded"] is False
    d = watchdog(False, True, True, True)
    assert d["learned_stale"] is True and d["deterministic_alerts"] is True
    assert watchdog(True, False, True, True)["pause_promotion"] is True
    assert watchdog(True, True, False, True)["no_approvals_actions"] is True


def test_perf_report_requires_conditions():
    with pytest.raises(ValueError):
        perf_report("local", {}, {"rps": 50}, [])
    r = perf_report("local", {"api": "0.1"}, {"warmup_s": 300, "duration_s": 1800, "rps": 50, "payload_kb": 10}, [])
    assert r["topology"] == "local"
