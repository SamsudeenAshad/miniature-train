"""Contracts skeleton checks (SRS 10.x)."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_openapi_skeleton():
    doc = yaml.safe_load((ROOT / "packages/contracts/openapi-v1.yaml").read_text())
    assert doc["openapi"].startswith("3.")
    paths = doc["paths"]
    assert "/health/live" in paths
    assert "/health/ready" in paths
    assert any(k.startswith("/v1/projects") for k in paths)


def test_anomaly_event_example():
    evt = json.loads((ROOT / "packages/contracts/events/anomaly.detected.json").read_text())
    for k in ("schema_version", "event_id", "event_type", "project_id", "payload"):
        assert k in evt
    assert evt["payload"]["score_semantics"] == "normalized_anomaly_score_not_probability"


def test_inference_contract_parses():
    doc = yaml.safe_load((ROOT / "packages/contracts/inference-openapi.yaml").read_text())
    assert doc["openapi"].startswith("3.")
    assert doc["info"]["version"] == "0.2.0"
