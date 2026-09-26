"""Control API (SRS 8.2, FR-001/002, FR-038). Membership enforced server-side.

Pilot identity: X-Subject/X-Role headers stand in for OIDC claims.
Reads use stored membership, never the presented role.
"""

import importlib.util
from pathlib import Path

from fastapi import FastAPI, Header, Response, status
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[3]


def _load(mod: str, rel: str):
    spec = importlib.util.spec_from_file_location(mod, str(ROOT / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_authz = _load("authz", "services/control-api/authz.py")
_idem = _load("apicontracts", "services/control-api/contracts.py")
_store_mod = _load("store", "services/control-api/app/store.py")
app = FastAPI(title="miniature-train control API", version="0.1.0")

_store = _store_mod.MemoryStore()
_projects = _store.projects
_members = _store.members


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
                   x_role: str = Header(default=""),
                   idempotency_key: str = Header(default="")):
    if x_role != "project_admin":
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"code": "forbidden", "message": "project creation requires admin", "retryable": False}
    if idempotency_key:
        try:
            prior = _idem.submit(idempotency_key, {"name": body.name, "owner": body.owner})
            if prior.get("project_id"):
                response.status_code = status.HTTP_200_OK
                return _projects[prior["project_id"]]
        except ValueError:
            response.status_code = status.HTTP_409_CONFLICT
            return {"code": "conflict", "message": "idempotency key reused with different payload",
                    "retryable": False}
    pid = f"proj_{len(_projects) + 1}"
    _projects[pid] = {"id": pid, "name": body.name, "owner": body.owner}
    _members[pid] = {x_subject or body.owner: "project_admin", body.owner: "project_admin"}
    if idempotency_key:
        _idem.attach(idempotency_key, "project_id", pid)
    return _projects[pid]


@app.get("/v1/projects/{project_id}/overview")
def overview(project_id: str, response: Response, x_subject: str = Header(default="")):
    role = _members.get(project_id, {}).get(x_subject)
    if not role or not _authz.can(role, "read", project_id, project_id):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"code": "not_found", "message": "project absent or concealed", "retryable": False}
    return {"project": _projects[project_id], "freshness": "current", "backend": _store.backend}


def reset() -> None:
    _store.reset()
    _idem.reset()
