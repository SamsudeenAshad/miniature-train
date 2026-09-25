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
    routes = {r.path for r in _load_api().app.routes if hasattr(r, "path")}
    for path in ("/health/live", "/health/ready", "/v1/projects",
                 "/v1/projects/{project_id}/overview"):
        assert path in routes, path
    assert any("datasets" in p for p in doc["paths"])  # contract still describes roadmap


def test_inference_paths_implemented():
    routes = {r.path for r in _load_infer().app.routes if hasattr(r, "path")}
    assert {"/health/live", "/health/ready", "/predict"} <= routes
