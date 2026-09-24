"""Backup manifest tests (Step 40)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_backup_schedule_and_runbook():
    cj = yaml.safe_load((ROOT / "infra/k8s/backup-cronjob.yaml").read_text())
    assert cj["spec"]["schedule"] == "0 2 * * *"
    assert "RTO" in (ROOT / "docs/restore-runbook.md").read_text() or "rto" in (ROOT / "docs/restore-runbook.md").read_text().lower()
