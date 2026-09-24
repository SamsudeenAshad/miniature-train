"""Training identity tests (Step 91). No API access for batch compute."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_training_locked_down():
    wf = yaml.safe_load((ROOT / "infra/workflows/training-dag.yaml").read_text())
    assert wf["spec"]["serviceAccountName"] == "training"
    sa = yaml.safe_load((ROOT / "infra/k8s/training-sa.yaml").read_text())
    assert sa["automountServiceAccountToken"] is False
