"""Job lockdown tests (Step 92). Batch pods get no API tokens."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _pod(d):
    s = d["spec"]
    if d["kind"] == "CronJob":
        s = s["jobTemplate"]["spec"]
    return s["template"]["spec"]


def test_jobs_tokenless():
    for f in ("backup-cronjob.yaml", "bucket-job.yaml"):
        for d in yaml.safe_load_all((ROOT / f).read_text()):
            if d and d.get("kind") in ("Job", "CronJob"):
                assert _pod(d).get("automountServiceAccountToken") is False, f
