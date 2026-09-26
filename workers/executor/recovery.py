"""Runbook + policy + fenced execution (FR-027/028/029, NFR-010 slice)."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import yaml

_POLICY = yaml.safe_load((Path(__file__).resolve().parents[2] / "policies/action-policy.yaml").read_text())

APPROVAL_TTL_S = int(_POLICY["approval_ttl_s"])
EVIDENCE_TTL_S = int(_POLICY["evidence_ttl_s"])
COOLDOWN_S = int(_POLICY["cooldown_s"])

RUNBOOKS = {
    "rollback-release": {"version": 1, "risk": "medium", "targets": ("staging", "prod-like")},
    "restart-replica": {"version": 1, "risk": "medium", "targets": ("staging", "prod-like")},
}

_locks: dict[str, str] = {}
_last_action: dict[str, float] = {}
_idem: dict[str, dict] = {}


def reset() -> None:
    _locks.clear()
    _last_action.clear()
    _idem.clear()


def dry_run(runbook: str, target: str, params: dict) -> dict:
    spec = RUNBOOKS.get(runbook)
    if spec is None:
        raise ValueError("unknown_runbook")
    if target not in spec["targets"]:
        raise ValueError("target_not_allowed")
    plan = {"runbook": runbook, "version": spec["version"], "target": target, "params": params}
    plan["plan_hash"] = hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()
    return plan


def check_policy(plan: dict, approval: dict, evidence_ts: float, kill_switch: bool, now: float | None = None) -> dict:
    now = now if now is not None else time.time()
    if kill_switch:
        return {"allow": False, "reason": "kill_switch"}
    if approval.get("plan_hash") != plan["plan_hash"]:
        return {"allow": False, "reason": "plan_mismatch"}
    if approval.get("approver") == approval.get("requester"):
        return {"allow": False, "reason": "self_approval"}
    if now - approval.get("ts", 0) > APPROVAL_TTL_S:
        return {"allow": False, "reason": "stale_approval"}
    if now - evidence_ts > EVIDENCE_TTL_S:
        return {"allow": False, "reason": "stale_evidence"}
    if _locks.get(plan["target"]):
        return {"allow": False, "reason": "target_locked"}
    if now - _last_action.get(plan["target"], 0) < COOLDOWN_S:
        return {"allow": False, "reason": "cooldown"}
    return {"allow": True, "reason": "ok"}


def execute(plan: dict, idempotency_key: str, fencing_token: str) -> dict:
    if idempotency_key in _idem:
        return _idem[idempotency_key]
    if _locks.get(plan["target"]) and _locks[plan["target"]] != fencing_token:
        return {"status": "rejected", "reason": "fencing_conflict"}
    _locks[plan["target"]] = fencing_token
    try:
        result = {"status": "succeeded", "plan_hash": plan["plan_hash"], "fencing_token": fencing_token}
        _idem[idempotency_key] = result
        _last_action[plan["target"]] = time.time()
        return result
    finally:
        _locks.pop(plan["target"], None)
