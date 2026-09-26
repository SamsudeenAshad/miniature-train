"""Workflow manifest tests (Step 35, WBS 4.1/ADR-08 slice)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/workflows"


def test_dag_order_and_budgets():
    wf = yaml.safe_load((ROOT / "training-dag.yaml").read_text())
    assert wf["spec"]["podSecurityContext"]["seccompProfile"] == {"type": "RuntimeDefault"}
    dag = next(t for t in wf["spec"]["templates"] if t["name"] == "pipeline")["dag"]["tasks"]
    order = [t["name"] for t in dag]
    assert order == ["validate", "train", "evaluate", "register"]
    step = next(t for t in wf["spec"]["templates"] if t["name"] == "step")
    assert step["retryStrategy"]["limit"] == 2
    assert wf["spec"]["activeDeadlineSeconds"] == 7200
