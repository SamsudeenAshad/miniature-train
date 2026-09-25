"""Secret reference tests (Step 113). Every secretKeyRef resolves to an ExternalSecret key."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _docs():
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d:
                yield f.name, d


def _pod(d):
    s = d["spec"]
    if d["kind"] == "CronJob":
        s = s["jobTemplate"]["spec"]
    return s["template"]["spec"]


def _env_refs(pod):
    for c in pod.get("containers", []):
        for e in c.get("env", []):
            ref = (e.get("valueFrom") or {}).get("secretKeyRef")
            if ref:
                yield ref["name"], ref["key"]


def test_secret_refs_resolve():
    provided = {}
    for _, d in _docs():
        if d.get("kind") == "ExternalSecret":
            provided[d["spec"]["target"]["name"]] = {r["secretKey"] for r in d["spec"]["data"]}
    assert provided, "no ExternalSecrets found"
    missing = []
    for fname, d in _docs():
        if d.get("kind") not in ("Deployment", "StatefulSet", "Job", "CronJob"):
            continue
        for name, key in _env_refs(_pod(d)):
            if key not in provided.get(name, set()):
                missing.append((fname, name, key))
    assert not missing, missing
