"""Container hardening tests (Step 41, SRS 13.4 slice)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_nonroot_scoped_sa():
    dep = yaml.safe_load((ROOT / "control-api.yaml").read_text())
    spec = dep["spec"]["template"]["spec"]
    assert spec["serviceAccountName"] == "control-api"
    sc = spec["containers"][0]["securityContext"]
    assert sc["runAsNonRoot"] is True
    assert sc["readOnlyRootFilesystem"] is True
    sa = yaml.safe_load((ROOT / "serviceaccount.yaml").read_text())
    assert sa["metadata"]["namespace"] == "miniature-train"
