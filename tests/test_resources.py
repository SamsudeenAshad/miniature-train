"""Resource bound tests (Step 95). Every container declares requests and limits."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _containers():
    for f in sorted((ROOT / "infra/k8s").glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if not d or d.get("kind") not in ("Deployment", "StatefulSet", "Job", "CronJob"):
                continue
            s = d["spec"]
            if d["kind"] == "CronJob":
                s = s["jobTemplate"]["spec"]
            pod = s["template"]["spec"] if d["kind"] in ("Job", "CronJob") else s["template"]["spec"]
            for c in pod.get("containers", []):
                yield f.name, c.get("name"), c.get("resources", {})
    for d in yaml.safe_load_all(((ROOT / "infra/workflows/training-dag.yaml").read_text())):
        for t in d["spec"].get("templates", []):
            if "container" in t:
                yield "training-dag.yaml", t["name"], t["container"].get("resources", {})


def test_requests_and_limits_everywhere():
    found = list(_containers())
    assert len(found) >= 14
    for fname, name, res in found:
        assert "requests" in res and "limits" in res, f"{fname} {name}"
