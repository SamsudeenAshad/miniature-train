"""Control API (SRS 8.2, FR-001/002, FR-038). Authz enforced per-object in later slice."""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI(title="miniature-train control API", version="0.1.0")

_projects: dict[str, dict] = {}


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
def create_project(body: ProjectIn):
    pid = f"proj_{len(_projects) + 1}"
    _projects[pid] = {"id": pid, "name": body.name, "owner": body.owner}
    return _projects[pid]


@app.get("/v1/projects/{project_id}/overview")
def overview(project_id: str, response: Response):
    if project_id not in _projects:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"code": "not_found", "message": "project absent or concealed", "retryable": False}
    return {"project": _projects[project_id], "freshness": "current"}


def reset() -> None:
    _projects.clear()
