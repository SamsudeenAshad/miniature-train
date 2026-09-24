"""Executor RBAC tests (Step 80). Least privilege: no secrets, no delete, no cluster scope."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_executor_bounded():
    docs = list(yaml.safe_load_all((ROOT / "executor-rbac.yaml").read_text()))
    role = next(d for d in docs if d["kind"] == "Role")
    verbs = {v for r in role["rules"] for v in r["verbs"]}
    assert verbs <= {"get", "list", "patch"}
    assert "secrets" not in str(role["rules"])
    assert role["metadata"]["namespace"] == "miniature-train"
    assert all(d["metadata"]["namespace"] == "miniature-train" for d in docs)
