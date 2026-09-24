"""Inference identity tests (Step 55)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_dedicated_sa_least_privilege():
    docs = list(yaml.safe_load_all((ROOT / "inference-rbac.yaml").read_text()))
    kinds = {d["kind"] for d in docs}
    assert {"ServiceAccount", "Role", "RoleBinding"} <= kinds
    role = next(d for d in docs if d["kind"] == "Role")
    assert role["rules"] == [{"apiGroups": [""], "resources": ["configmaps"], "verbs": ["get", "list"]}]
