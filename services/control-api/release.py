"""Release promotion state machine (FR-013 slice, SRS 11.2).

Staging -> shadow -> approve (independent) -> promote -> rollback.
Shadow responses never reach users. Missing/failed gates block promotion.
"""

from __future__ import annotations


def propose(model_version: int, artifact_digest: str, requester: str) -> dict:
    return {
        "model_version": model_version,
        "artifact_digest": artifact_digest,
        "requester": requester,
        "state": "proposed",
        "approver": None,
        "previous_digest": None,
    }


def approve(release: dict, approver: str, gates_pass: bool) -> dict:
    if not gates_pass:
        raise ValueError("gates_failed")
    if approver == release["requester"]:
        raise ValueError("self_approval_blocked")
    release = dict(release, state="approved", approver=approver)
    return release


def promote(release: dict, previous_digest: str, shadow_ok: bool) -> dict:
    if release["state"] != "approved":
        raise ValueError("not_approved")
    if not shadow_ok:
        raise ValueError("shadow_failed")
    return dict(release, state="promoted", previous_digest=previous_digest)


def rollback(release: dict) -> dict:
    if release["state"] != "promoted":
        raise ValueError("nothing_to_rollback")
    if not release.get("previous_digest"):
        raise ValueError("no_compatible_previous")
    return dict(release, state="rolled_back", artifact_digest=release["previous_digest"])
