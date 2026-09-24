"""DB manifest tests (Step 59)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_db_singleton_spof_noted():
    docs = list(yaml.safe_load_all((ROOT / "db.yaml").read_text()))
    sts = next(d for d in docs if d["kind"] == "StatefulSet")
    assert sts["spec"]["replicas"] == 1  # honest SPOF: single database
    env = sts["spec"]["template"]["spec"]["containers"][0]["env"]
    assert any(e.get("valueFrom", {}).get("secretKeyRef", {}).get("key") == "database-password" for e in env)
