"""Control API env tests (Step 74). DB wiring matches db service + secret."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_api_db_env():
    dep = yaml.safe_load((ROOT / "control-api.yaml").read_text())
    env = {e["name"]: e for e in dep["spec"]["template"]["spec"]["containers"][0]["env"]}
    assert env["POSTGRES_HOST"]["value"] == "db"
    ref = env["POSTGRES_PASSWORD"]["valueFrom"]["secretKeyRef"]
    assert (ref["name"], ref["key"]) == ("control-api", "database-password")
    es = yaml.safe_load((ROOT / "externalsecret.yaml").read_text())
    assert es["spec"]["target"]["name"] == "control-api"
