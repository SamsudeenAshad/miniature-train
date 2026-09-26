"""OpenAPI parity tests (Step 118). Documented paths must exist in code."""

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_api():
    spec = importlib.util.spec_from_file_location("api_main", str(ROOT / "services/control-api/app/main.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_infer():
    spec = importlib.util.spec_from_file_location("infer_main", str(ROOT / "services/inference/app/main.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_control_paths_implemented():
    doc = yaml.safe_load((ROOT / "packages/contracts/openapi-v1.yaml").read_text())
    assert doc["info"]["version"] == "0.2.0"
    api = _load_api()
    assert api.app.version == doc["info"]["version"]
    routes = {r.path for r in _load_api().app.routes if hasattr(r, "path")}
    for path in ("/health/live", "/health/ready", "/v1/projects",
                 "/v1/projects/{project_id}/overview"):
        assert path in routes, path
    create_responses = set(doc["paths"]["/v1/projects"]["post"]["responses"])
    assert {"200", "201", "403", "409"} <= create_responses
    overview = doc["paths"]["/v1/projects/{project_id}/overview"]["get"]
    assert "404" in overview["responses"]
    assert any(p.get("in") == "header" and p.get("name") == "X-Subject"
               for p in overview["parameters"])
    assert any("datasets" in p for p in doc["paths"])  # contract still describes roadmap


def test_inference_paths_implemented():
    infer = _load_infer()
    routes = {r.path for r in infer.app.routes if hasattr(r, "path")}
    assert {"/health/live", "/health/ready", "/predict"} <= routes
    assert infer.app.version == "0.2.0"
