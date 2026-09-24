"""Controlled recovery tests (FR-027/028/029, NFR-010 slice)."""

import time

from workers.executor.recovery import check_policy, dry_run, execute, reset


def _approval(plan, requester="op", approver="owner", age_s=10):
    return {"plan_hash": plan["plan_hash"], "requester": requester, "approver": approver, "ts": time.time() - age_s}


def test_dry_run_exact_plan_no_mutation():
    reset()
    p1 = dry_run("rollback-release", "staging", {"rev": "abc"})
    p2 = dry_run("rollback-release", "staging", {"rev": "abc"})
    assert p1 == p2
    assert "plan_hash" in p1


def test_policy_denies_by_default():
    reset()
    plan = dry_run("rollback-release", "staging", {"rev": "abc"})
    assert check_policy(plan, _approval(plan, approver="op"), time.time(), False)["reason"] == "self_approval"
    assert check_policy(plan, _approval(plan, age_s=3600), time.time(), False)["reason"] == "stale_approval"
    assert check_policy(plan, _approval(plan), time.time() - 600, False)["reason"] == "stale_evidence"
    assert check_policy(plan, _approval(plan), time.time(), True)["reason"] == "kill_switch"


def test_idempotent_no_duplicate_side_effects():
    reset()
    plan = dry_run("restart-replica", "staging", {"replica": "a"})
    ap = _approval(plan)
    assert check_policy(plan, ap, time.time(), False)["allow"] is True
    r1 = execute(plan, "key-1", "fence-1")
    r2 = execute(plan, "key-1", "fence-1")
    assert r1 == r2 == {"status": "succeeded", "plan_hash": plan["plan_hash"], "fencing_token": "fence-1"}
