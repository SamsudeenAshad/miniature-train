"""Control API HTTP tests (Step 51, FR-002/038 slice)."""

import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("api_main", str(ROOT / "services/control-api/app/main.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_health_and_projects():
    m = _load()
    m.reset()
    c = TestClient(m.app)
    assert c.get("/health/live").json() == {"status": "alive"}
    assert c.post("/v1/projects", json={"name": "demo", "owner": "owner-1"}).status_code == 403
    r = c.post("/v1/projects", json={"name": "demo", "owner": "owner-1"},
               headers={"X-Subject": "admin-1", "X-Role": "project_admin"})
    assert r.status_code == 201
    pid = r.json()["id"]
    assert c.get(f"/v1/projects/{pid}/overview", headers={"X-Subject": "owner-1"}).status_code == 200
    assert c.get(f"/v1/projects/{pid}/overview", headers={"X-Subject": "stranger"}).status_code == 404
    assert c.get("/v1/projects/nope/overview", headers={"X-Subject": "owner-1"}).status_code == 404
