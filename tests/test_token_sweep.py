"""Token choice tests (Steps 93, 179). Every workload declares automount explicitly; all false."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"
WORKFLOWS = Path(__file__).resolve().parents[1] / "infra/workflows"


def _pods():
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if not d or d.get("kind") not in ("Deployment", "StatefulSet", "Job", "CronJob"):
                continue
            s = d["spec"]
            if d["kind"] == "CronJob":
                s = s["jobTemplate"]["spec"]
            if d["kind"] in ("Job", "CronJob"):
                yield f.name, d["metadata"]["name"], s["template"]["spec"]
            else:
                yield f.name, d["metadata"]["name"], s["template"]["spec"]


def test_explicit_tokenless_everywhere():
    pods = list(_pods())
    assert len(pods) >= 10
    for fname, name, pod in pods:
        assert pod.get("automountServiceAccountToken") is False, f"{fname} {name}"
    tokenless_sas = set()
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") == "ServiceAccount" and d.get("automountServiceAccountToken") is False:
                tokenless_sas.add(d["metadata"]["name"])
    for f in sorted(WORKFLOWS.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") == "WorkflowTemplate":
                sa = d["spec"].get("serviceAccountName")
                assert sa in tokenless_sas, f"{f.name} uses tokened SA {sa}"
