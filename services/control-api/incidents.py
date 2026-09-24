"""Incident lifecycle (FR-026 slice, WBS 6.2/9.2).

Severity/owner/timeline/ack/investigate/resolve/reopen/close.
Transitions need permission + reason + expected version (optimistic
locking). Resolution requires recovery evidence.
"""

from __future__ import annotations


def create(severity: str, owner: str) -> dict:
    return {"state": "open", "severity": severity, "owner": owner, "version": 1, "timeline": ["opened"]}


def transition(inc: dict, to: str, actor_role: str, reason: str, expected_version: int, evidence: bool = False) -> dict:
    allowed_roles = {"operator", "project_admin"}
    if actor_role not in allowed_roles:
        raise ValueError("forbidden")
    if not reason:
        raise ValueError("reason_required")
    if expected_version != inc["version"]:
        raise ValueError("stale_version")
    if to == "resolved" and not evidence:
        raise ValueError("evidence_required")
    if to == "closed" and inc["state"] != "resolved":
        raise ValueError("must_resolve_first")
    return dict(inc, state=to, version=inc["version"] + 1, timeline=inc["timeline"] + [to])
