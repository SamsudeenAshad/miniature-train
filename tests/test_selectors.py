"""Service selector tests (Step 114). Every selector matches at least one pod template."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _docs():
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d:
                yield f.name, d


def test_selectors_match_pods():
    labels = []
    for _, d in _docs():
        if d.get("kind") in ("Deployment", "StatefulSet"):
            labels.append((d["metadata"]["name"], d["spec"]["template"]["metadata"]["labels"]))
    assert labels, "no pod templates found"
    bound_apps = set()
    for fname, d in _docs():
        if d.get("kind") == "Rollout" and "workloadRef" in d.get("spec", {}):
            for wname, lbs in labels:
                if d["spec"]["workloadRef"].get("name") == wname:
                    bound_apps.add(lbs.get("app"))
    unmatched = []
    for fname, d in _docs():
        if d.get("kind") != "Service":
            continue
        sel = d["spec"]["selector"]
        if sel.get("track") == "canary":
            # canary endpoints exist only during progression; the app must be rollout-managed
            if sel.get("app") not in bound_apps:
                unmatched.append((fname, d["metadata"]["name"], sel))
        elif not any(all(lbs.get(k) == v for k, v in sel.items()) for _, lbs in labels):
            unmatched.append((fname, d["metadata"]["name"], sel))
    assert not unmatched, unmatched
