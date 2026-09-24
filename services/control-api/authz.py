"""Server-side authorization (FR-001/002 slice, SRS 3.2). UI visibility is not a boundary."""

from __future__ import annotations

# role -> allowed actions (project-scoped; platform-admin needs explicit grant)
ALLOW = {
    "viewer": {"read"},
    "ml_engineer": {"read", "register_dataset", "submit_run", "propose_release", "comment_incident"},
    "operator": {"read", "propose_release", "ack_incident", "propose_action"},
    "project_admin": {"read", "register_dataset", "submit_run", "propose_release", "ack_incident",
                      "propose_action", "approve_release", "approve_action", "manage_policy"},
}


def can(role: str, action: str, project: str, scope_project: str) -> bool:
    if project != scope_project:
        return False
    return action in ALLOW.get(role, set())


def can_approve(role: str, requester: str, approver: str, delegated: bool = False) -> bool:
    if requester == approver:
        return False
    if role == "project_admin":
        return True
    if role == "operator" and delegated:
        return True
    return False
