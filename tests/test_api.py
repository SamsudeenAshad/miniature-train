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
    assert c.get("/health/ready").json() == {"status": "ready", "store": "memory"}
    assert c.post("/v1/projects", json={"name": "demo", "owner": "owner-1"}).status_code == 403
    r = c.post("/v1/projects", json={"name": "demo", "owner": "owner-1"},
               headers={"X-Subject": "admin-1", "X-Role": "project_admin"})
    assert r.status_code == 201
    pid = r.json()["id"]
    body = c.get(f"/v1/projects/{pid}/overview", headers={"X-Subject": "owner-1"}).json()
    assert body["freshness"] == "current" and body["backend"] == "memory"
    assert c.get(f"/v1/projects/{pid}/overview", headers={"X-Subject": "stranger"}).status_code == 404
    assert c.get("/v1/projects/nope/overview", headers={"X-Subject": "owner-1"}).status_code == 404


def test_project_idempotency():
    m = _load()
    m.reset()
    c = TestClient(m.app)
    h = {"X-Subject": "admin-1", "X-Role": "project_admin", "Idempotency-Key": "k-1"}
    r1 = c.post("/v1/projects", json={"name": "demo", "owner": "owner-1"}, headers=h)
    r2 = c.post("/v1/projects", json={"name": "demo", "owner": "owner-1"}, headers=h)
    assert r1.status_code == 201
    assert r2.status_code == 200
    assert r1.json()["id"] == r2.json()["id"]
    assert r1.headers["location"] == r2.headers["location"] == f"/v1/projects/{r1.json()['id']}"
    r3 = c.post("/v1/projects", json={"name": "other", "owner": "owner-1"}, headers=h)
    assert r3.status_code == 409
    r4 = c.post("/v1/projects", json={"name": "other", "owner": "owner-1"},
                headers={"Idempotency-Key": "k-1"})
    assert r4.status_code == 403


def test_validation_error_envelope():
    m = _load()
    m.reset()
    c = TestClient(m.app)
    r = c.post("/v1/projects", json={"name": "broken"},
               headers={"X-Subject": "admin-1", "X-Role": "project_admin"})
    assert r.status_code == 422
    body = r.json()
    assert set(body) >= {"code", "message", "request_id", "retryable"}
    assert body["code"] == "unprocessable" and body["retryable"] is False


def test_missing_identity_headers_denied():
    m = _load()
    m.reset()
    c = TestClient(m.app)
    assert c.get("/v1/projects/proj_9/overview").status_code == 404
    assert c.post("/v1/projects", json={"name": "demo", "owner": "o"}).status_code == 403
    non_admin = {"X-Subject": "op-1", "X-Role": "operator"}
    assert c.post("/v1/projects", json={"name": "demo", "owner": "o"},
                  headers=non_admin).status_code == 403
