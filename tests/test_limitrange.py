"""LimitRange tests (Step 83). Defaults inside the quota envelope, max matches task cap."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_limits_bounded():
    lr = yaml.safe_load((ROOT / "limitrange.yaml").read_text())
    entry = lr["spec"]["limits"][0]
    assert entry["max"] == {"cpu": "2", "memory": "4Gi"}
    assert entry["defaultRequest"] == {"cpu": "100m", "memory": "128Mi"}
