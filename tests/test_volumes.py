"""Volume audit tests (Step 90). Every referenced config file and claim is mounted."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _pod(d):
    s = d["spec"]
    if d["kind"] == "CronJob":
        s = s["jobTemplate"]["spec"]
    if d["kind"] in ("Job", "CronJob"):
        return s["template"]["spec"]
    return s["template"]["spec"]


def _deployments():
    out = []
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") in ("Deployment", "StatefulSet"):
                out.append((f.name, d))
    return out


def test_claims_and_configs_mounted():
    for fname, d in _deployments():
        pod = _pod(d)
        mounts = {m["name"] for c in pod.get("containers", []) for m in c.get("volumeMounts", [])}
        vols = {v["name"] for v in pod.get("volumes", [])}
        claims = {v["metadata"]["name"] for v in d["spec"].get("volumeClaimTemplates", [])}
        for arg in [a for c in pod.get("containers", []) for a in c.get("args", [])]:
            if arg.startswith("-config.file="):
                assert "config" in mounts, f"{fname} {d['metadata']['name']}: config arg without mount"
        assert claims <= mounts | vols, f"{fname} {d['metadata']['name']}: unmounted claim {claims - mounts - vols}"
