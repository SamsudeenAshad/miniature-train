"""Abort + reconciliation (FR-015, NFR-006 slice, WBS 5.4).

Abort a failing rollout and restore a compatible known-good release.
Verified only when Git state, router state, model version, and actual
workload converge. Incompatible schema or missing prior artifact blocks
unsafe automatic rollback with an escalated incident.
"""

from __future__ import annotations


def request_abort(rollout: dict, guard_failed: bool, enrolled: bool) -> dict:
    if not enrolled:
        return {"action": "escalate", "reason": "guard_not_enrolled"}
    if not guard_failed:
        return {"action": "hold", "reason": "guard_passing"}
    return {"action": "abort", "reason": "guard_failed", "rollout": rollout["id"]}


def restore_known_good(rollout: dict, prior: dict | None) -> dict:
    if prior is None:
        return {"state": "escalated", "reason": "prior_artifact_unavailable"}
    if prior.get("schema") != rollout.get("schema"):
        return {"state": "blocked", "reason": "incompatible_schema"}
    return {"state": "restoring", "digest": prior["digest"]}


def reconcile(git_rev: str, observed_rev: str, router: str, expected_router: str, model: str, expected_model: str) -> dict:
    if git_rev == observed_rev and router == expected_router and model == expected_model:
        return {"state": "verified"}
    return {"state": "reconciliation_required"}
