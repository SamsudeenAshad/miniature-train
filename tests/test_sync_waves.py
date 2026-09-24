"""Sync-wave tests (Step 99). Data layer syncs before apps."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _waves():
    out = {}
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") in ("StatefulSet", "Deployment", "Job"):
                out[d["metadata"]["name"]] = d["metadata"].get("annotations", {}).get(
                    "argocd.argoproj.io/sync-wave", "1")
    return out


def test_data_layer_first():
    waves = _waves()
    assert waves["db"] == "0" and waves["object-store"] == "0"
    assert all(w >= "0" for w in waves.values())
