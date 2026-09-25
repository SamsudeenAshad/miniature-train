"""Quota parity tests (Step 133). Workflow budgets match versioned policy caps."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_workflow_within_policy():
    quotas = yaml.safe_load((ROOT / "policies/quotas.yaml").read_text())
    wf = yaml.safe_load((ROOT / "infra/workflows/training-dag.yaml").read_text())
    step = next(t for t in wf["spec"]["templates"] if t["name"] == "step")
    res = step["container"]["resources"]
    assert res["requests"]["cpu"] == str(quotas["training_task_cpu"])
    assert res["requests"]["memory"] == f"{quotas['training_task_mem_gb']}Gi"
    assert wf["spec"]["activeDeadlineSeconds"] <= 7200
