"""Istio routing tests (Step 61)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_virtual_service_matches_rollout():
    vs = yaml.safe_load((ROOT / "virtualservice.yaml").read_text())
    routes = vs["spec"]["http"]
    assert [r["name"] for r in routes] == ["primary"]
    ro = yaml.safe_load((ROOT / "rollout.yaml").read_text())
    traffic = ro["spec"]["strategy"]["canary"]["trafficRouting"]["istio"]["virtualService"]
    assert traffic["name"] == "prediction-api"
    assert traffic["routes"] == ["primary"]
