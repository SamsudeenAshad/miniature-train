"""Harness tests (WBS 7.1 slice)."""

from workers.aiops.harness import plan_episodes


def test_episodes_frozen_and_spaced():
    p = plan_episodes(seed=5, per_family=6)
    assert len(p["episodes"]) == 30
    assert len(p["frozen_digest"]) == 64
    eps = sorted(p["episodes"], key=lambda e: e["start"])
    for a, b in zip(eps, eps[1:]):
        assert b["start"] - a["end"] >= 600
        assert 300 <= a["end"] - a["start"] <= 600
    assert plan_episodes(seed=5) == p
