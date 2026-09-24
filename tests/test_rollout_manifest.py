"""Rollout manifest tests (Step 33, SRS 11.3 slice)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_rollout_steps_match_policy():
    ro = yaml.safe_load((ROOT / "rollout.yaml").read_text())
    weights = [s["setWeight"] for s in ro["spec"]["strategy"]["canary"]["steps"] if "setWeight" in s]
    assert weights == [5, 25, 50, 100]
    assert ro["spec"]["workloadRef"] == {"apiVersion": "apps/v1", "kind": "Deployment", "name": "inference"}
    assert ro["spec"]["selector"]["matchLabels"] == {"app": "inference"}
    at = yaml.safe_load((ROOT / "analysistemplate.yaml").read_text())
    names = {m["name"] for m in at["spec"]["metrics"]}
    assert {"error-rate", "p95-latency"} <= names
