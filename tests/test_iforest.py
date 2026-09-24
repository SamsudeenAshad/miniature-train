"""Challenger adapter tests (SRS 7.1/7.2 slice)."""

from workers.aiops import iforest


def test_challenger_contract_or_unavailable():
    r = iforest.detect([{"value": 1.0}])
    assert r["score_semantics"] == "normalized_anomaly_score_not_probability"
    assert r["detector_version"] == "iforest-1.0"
