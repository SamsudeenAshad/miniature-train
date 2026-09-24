"""NetworkPolicy tests (Step 42, SRS 13.4 slice)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_default_deny_with_dns():
    np = yaml.safe_load((ROOT / "networkpolicy.yaml").read_text())
    assert set(np["spec"]["policyTypes"]) == {"Ingress", "Egress"}
    egress = np["spec"]["egress"]
    assert any("kube-dns" in str(e) for e in egress)
