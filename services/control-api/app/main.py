"""Control API (SRS 8.2, FR-001/002, FR-038). Membership enforced server-side.

Pilot identity: X-Subject/X-Role headers stand in for OIDC claims.
Reads use stored membership, never the presented role.
"""

import importlib.util
from pathlib import Path

from fastapi import FastAPI, Header, Response, status
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[3]


def _load_authz():
    spec = importlib.util.spec_from_file_location("authz", str(ROOT / "services/control-api/authz.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_authz = _load_authz()
app = FastAPI(title="miniature-train control API", version="0.1.0")

_projects: dict[str, dict] = {}
_members: dict[str, dict[str, str]] = {}


class ProjectIn(BaseModel):
    name: str
    owner: str


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready", "deps": "skeleton"}


@app.post("/v1/projects", status_code=201)
def create_project(body: ProjectIn, response: Response,
                   x_subject: str = Header(default=""),
                   x_role: str = Header(default="")):
    if x_role != "project_admin":
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"code": "forbidden", "message": "project creation requires admin", "retryable": False}
    pid = f"proj_{len(_projects) + 1}"
    _projects[pid] = {"id": pid, "name": body.name, "owner": body.owner}
    _members[pid] = {x_subject or body.owner: "project_admin", body.owner: "project_admin"}
    return _projects[pid]


@app.get("/v1/projects/{project_id}/overview")
def overview(project_id: str, response: Response, x_subject: str = Header(default="")):
    role = _members.get(project_id, {}).get(x_subject)
    if not role or not _authz.can(role, "read", project_id, project_id):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"code": "not_found", "message": "project absent or concealed", "retryable": False}
    return {"project": _projects[project_id], "freshness": "current"}


def reset() -> None:
    _projects.clear()
    _members.clear()
