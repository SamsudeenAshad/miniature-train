"""ConfigMap reference tests (Step 112). Every mounted ConfigMap must exist."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _docs():
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d:
                yield f.name, d


def test_configmap_refs_resolve():
    defined = {d["metadata"]["name"] for _, d in _docs() if d.get("kind") == "ConfigMap"}
    missing = []
    for fname, d in _docs():
        if d.get("kind") not in ("Deployment", "StatefulSet", "Job", "CronJob"):
            continue
        s = d["spec"]
        if d["kind"] == "CronJob":
            s = s["jobTemplate"]["spec"]
        pod = s["template"]["spec"]
        for v in pod.get("volumes", []):
            if "configMap" in v and v["configMap"]["name"] not in defined:
                missing.append((fname, v["configMap"]["name"]))
    assert not missing, missing
