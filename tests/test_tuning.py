"""Tuning + artifact trust tests (FR-008/012 slice)."""

from ml.artifacts import verify_artifact
from ml.tuning import MAX_TRIALS, search


def test_search_bounded_no_autopromote():
    space = {"lr": [0.01, 0.05, 0.1, 0.2], "depth": [3, 5, 7, 9]}
    r = search(space, seed=1, max_trials=MAX_TRIALS)
    assert r["count"] <= MAX_TRIALS
    assert r["auto_promoted"] is False
    assert r["truncated"] is True
    r2 = search(space, seed=1, max_trials=MAX_TRIALS)
    assert r == r2


def test_artifact_trust():
    assert verify_artifact("d", "sig", "ml-pipeline", "none")["load"] is True
    assert verify_artifact("d", "sig", "random", "none")["load"] is False
    assert verify_artifact("d", "", "ml-pipeline", "none")["load"] is False
    assert verify_artifact("d", "sig", "ml-pipeline", "critical")["load"] is False
