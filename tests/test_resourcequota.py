"""Quota tests (Step 81, SRS 13.2/NFR-016 slice). Namespace envelope covers shared profile."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_quota_envelope():
    q = yaml.safe_load((ROOT / "infra/k8s/resourcequota.yaml").read_text())
    assert q["spec"]["hard"]["requests.cpu"] == "16"
    assert q["spec"]["hard"]["requests.memory"] == "32Gi"
    import yaml as y

    quotas = y.safe_load((ROOT / "policies/quotas.yaml").read_text())
    assert quotas["training_task_cpu"] == 2  # per-task cap inside the envelope
