"""K8s manifest tests (Step 30)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_manifests_parse_and_namespace():
    docs = {}
    for f in sorted(ROOT.glob("*.yaml")):
        docs[f.name] = yaml.safe_load(f.read_text())
    assert docs["namespace.yaml"]["kind"] == "Namespace"
    dep = docs["control-api.yaml"]
    assert dep["spec"]["template"]["spec"]["containers"][0]["image"].endswith(":v0.1.0")
    assert docs["service.yaml"]["kind"] == "Service"
