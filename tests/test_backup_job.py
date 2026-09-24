"""Backup image + job CLI tests (Step 76)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("restore", str(ROOT / "infra/restore.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_job_cli_matches_cronjob():
    import yaml

    cj = yaml.safe_load((ROOT / "infra/k8s/backup-cronjob.yaml").read_text())
    args = cj["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["args"]
    assert args == ["--rpo-hours=24", "--retain=30"]
    m = _load()
    assert m.main([]) == {"rpo_hours": 24, "retain": 30, "targets": ["metadata", "objects"]}
    assert m.main(["--rpo-hours=12"])["rpo_hours"] == 12
    df = (ROOT / "infra/docker/backup.Dockerfile").read_text()
    assert "ENTRYPOINT" in df and "USER 65532" in df
