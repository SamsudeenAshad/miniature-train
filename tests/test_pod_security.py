"""Pod security tests (Step 94). Restricted-standard seccomp on every pod spec."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


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


def test_seccomp_everywhere():
    pods = list(_pods())
    assert len(pods) >= 12
    for fname, name, pod in pods:
        sc = pod.get("securityContext", {})
        assert sc.get("seccompProfile", {}).get("type") == "RuntimeDefault", f"{fname} {name}"
