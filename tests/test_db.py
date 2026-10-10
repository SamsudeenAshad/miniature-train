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


def test_db_credentials_match_stack():
    docs = list(yaml.safe_load_all((ROOT / "db.yaml").read_text()))
    sts = next(d for d in docs if d["kind"] == "StatefulSet")
    env = {e["name"]: e for e in sts["spec"]["template"]["spec"]["containers"][0]["env"]}
    assert env["POSTGRES_USER"].get("value") == "mt"
    assert env["POSTGRES_DB"].get("value") == "mt"
    ref = env["POSTGRES_PASSWORD"]["valueFrom"]["secretKeyRef"]
    assert (ref["name"], ref["key"]) == ("control-api", "database-password")
