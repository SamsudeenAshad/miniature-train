"""LimitRange tests (Steps 83, 305). Defaults inside the quota envelope, max matches task cap."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_limits_bounded():
    lr = yaml.safe_load((ROOT / "limitrange.yaml").read_text())
    entry = lr["spec"]["limits"][0]
    quotas = yaml.safe_load((ROOT.parents[1] / "policies/quotas.yaml").read_text())
    assert entry["max"] == {"cpu": str(quotas["training_task_cpu"]),
                            "memory": f"{quotas['training_task_mem_gb']}Gi"}
    assert entry["defaultRequest"] == {"cpu": "100m", "memory": "128Mi"}
