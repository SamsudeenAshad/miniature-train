"""K8s manifest tests (Step 30)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_manifests_parse_and_namespace():
    docs = {}
    for f in sorted(ROOT.glob("*.yaml")):
        parsed = list(yaml.safe_load_all(f.read_text()))
        docs[f.name] = parsed[0] if len(parsed) == 1 else parsed
    assert docs["namespace.yaml"]["kind"] == "Namespace"
    dep = docs["control-api.yaml"]
    assert dep["spec"]["template"]["spec"]["containers"][0]["image"].endswith(":v0.19.0")
    assert docs["service.yaml"]["kind"] == "Service"
