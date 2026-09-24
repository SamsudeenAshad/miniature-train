"""Stable/canary service tests (Step 62)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_rollout_services_exist():
    docs = list(yaml.safe_load_all((ROOT / "prediction-services.yaml").read_text()))
    names = {d["metadata"]["name"] for d in docs}
    assert {"prediction-api-stable", "prediction-api-canary"} <= names
    ro = yaml.safe_load((ROOT / "rollout.yaml").read_text())
    canary = ro["spec"]["strategy"]["canary"]
    assert canary["stableService"] in names and canary["canaryService"] in names
