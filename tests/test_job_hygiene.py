"""Job hygiene tests (Step 126). One-shot jobs clean up and stop retrying."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_job_bounds():
    job = next(d for d in yaml.safe_load_all((ROOT / "bucket-job.yaml").read_text()) if d.get("kind") == "Job")
    assert job["spec"]["backoffLimit"] == 3
    assert job["spec"]["ttlSecondsAfterFinished"] == 3600
