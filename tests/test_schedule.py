"""Scheduling tests (SRS 13.2 slice)."""

from pathlib import Path

import yaml

from workers.training.schedule import admit_training

ROOT = Path(__file__).resolve().parents[1]


def test_queue_during_load():
    assert admit_training(True, 0)["decision"] == "queue"
    assert admit_training(True, 0, mixed=True)["decision"] == "start"
    assert admit_training(False, 5)["decision"] == "queue"
    assert admit_training(False, 0)["decision"] == "start"


def test_default_quota_matches_policy():
    import inspect

    quotas = yaml.safe_load((ROOT / "policies/quotas.yaml").read_text())
    default_quota = inspect.signature(admit_training).parameters["quota"].default
    assert default_quota == quotas["concurrent_training_tasks"]
