"""Harness tests (WBS 7.1 slice)."""

import pytest

from workers.aiops.harness import FAMILIES, plan_episodes


def test_episodes_frozen_and_spaced():
    p = plan_episodes(seed=5, per_family=6, allowlist=FAMILIES)
    assert len(p["episodes"]) == 30
    assert len(p["frozen_digest"]) == 64
    eps = sorted(p["episodes"], key=lambda e: e["start"])
    for a, b in zip(eps, eps[1:]):
        assert b["start"] - a["end"] >= 600
        assert 300 <= a["end"] - a["start"] <= 600
    assert plan_episodes(seed=5, allowlist=FAMILIES) == p


def test_allowlist_gates_injection():
    with pytest.raises(ValueError, match="allowlist_empty"):
        plan_episodes(seed=5)
    with pytest.raises(ValueError, match="unknown_families"):
        plan_episodes(seed=5, allowlist=("cpu", "nope"))
    scoped = plan_episodes(seed=5, per_family=2, allowlist=("cpu", "memory"))
    assert {e["family"] for e in scoped["episodes"]} == {"cpu", "memory"}
