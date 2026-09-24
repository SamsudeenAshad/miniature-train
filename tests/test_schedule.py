"""Scheduling tests (SRS 13.2 slice)."""

from workers.training.schedule import admit_training


def test_queue_during_load():
    assert admit_training(True, 0)["decision"] == "queue"
    assert admit_training(True, 0, mixed=True)["decision"] == "start"
    assert admit_training(False, 5)["decision"] == "queue"
    assert admit_training(False, 0)["decision"] == "start"
