"""AIOps detection/correlation/ranking tests (FR-022..025 slice)."""

from workers.aiops.correlate import correlate, rank_hypotheses
from workers.aiops.detect import detect


def test_detector_persistence():
    base = {"ref_mean": 100.0, "ref_std": 5.0}
    ok = detect([{"service": "api", "value": 101.0, **base}] * 3)
    assert ok["triggered"] is False
    bad = detect([{"service": "api", "value": 130.0, **base}] * 3)
    assert bad["triggered"] is True
    assert bad["score_semantics"] == "normalized_anomaly_score_not_probability"
    single = detect([{"service": "api", "value": 130.0, **base}])
    assert single["triggered"] is False  # needs 2-of-3


def test_correlation_groups_and_keeps_evidence():
    alerts = [
        {"service_group": "api", "ts": 0, "id": "a1"},
        {"service_group": "api", "ts": 60, "id": "a2"},
        {"service_group": "db", "ts": 70, "id": "b1"},
    ]
    incs = correlate(alerts)
    assert len(incs) == 2
    api = next(g for g in incs if g["service_group"] == "api")
    assert [a["id"] for a in api["alerts"]] == ["a1", "a2"]


def test_ranking_and_abstention():
    inc = {"incident_id": "inc_0"}
    ranked = rank_hypotheses(inc, [{"service": "api", "age_s": 120}], {"api": 0, "db": 1})
    assert ranked["status"] == "ranked"
    assert ranked["hypotheses"][0]["cause"] == "api"
    assert ranked["limitation"] == "correlation_not_causation"
    empty = rank_hypotheses(inc, [], {})
    assert empty["status"] == "abstained"
