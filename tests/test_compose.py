"""Compose tests (Step 166). Local-dev file is consistent and secret-free."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_compose_consistent():
    doc = yaml.safe_load((ROOT / "infra/docker-compose.yml").read_text())
    api = doc["services"]["control-api"]["build"]
    assert api["context"] == ".."
    assert (ROOT / api["dockerfile"]).exists()
    blob = (ROOT / "infra/docker-compose.yml").read_text()
    assert "POSTGRES_PASSWORD=mt" not in blob
    assert doc["services"]["db"]["image"] == "postgres:16.4"
    assert doc["services"]["control-api"]["depends_on"]["db"]["condition"] == "service_healthy"
    assert "pg_isready" in blob
    web = doc["services"]["web"]
    assert web["ports"] == ["8080:8080"]
    mounted = " ".join(str(v) for v in web.get("volumes", []))
    assert "nginx.compose.conf" in mounted
    for svc in ("control-api", "inference"):
        assert "healthcheck" in doc["services"][svc], svc
    assert "healthcheck" in doc["services"]["web"]
    for svc in ("control-api", "inference", "web"):
        assert doc["services"][svc].get("restart") == "unless-stopped", svc
    assert doc["services"]["db"].get("restart") == "always"
    deps = doc["services"]["web"]["depends_on"]
    assert deps["control-api"]["condition"] == "service_healthy"
    assert deps["inference"]["condition"] == "service_healthy"


def test_proxy_confs_agree_on_routes():
    k8s = (ROOT / "apps/web/nginx.conf").read_text()
    compose = (ROOT / "apps/web/nginx.compose.conf").read_text()
    for route in ("/api/control/", "/api/inference/"):
        assert route in k8s and route in compose
