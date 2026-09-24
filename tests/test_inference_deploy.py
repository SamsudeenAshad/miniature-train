"""Inference deploy tests (Step 54)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_inference_replicas_and_hardening():
    docs = list(yaml.safe_load_all((ROOT / "inference.yaml").read_text()))
    dep = next(d for d in docs if d["kind"] == "Deployment")
    assert dep["spec"]["replicas"] == 2
    sc = dep["spec"]["template"]["spec"]["containers"][0]["securityContext"]
    assert sc["runAsNonRoot"] is True
    svc = next(d for d in docs if d["kind"] == "Service")
    assert svc["spec"]["selector"] == {"app": "inference"}
