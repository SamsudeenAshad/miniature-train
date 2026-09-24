"""Training scheduling vs load tests (SRS 13.2 slice)."""

from __future__ import annotations


def admit_training(load_test_running: bool, running_train: int, quota: int = 2, mixed: bool = False) -> dict:
    if running_train >= quota:
        return {"decision": "queue", "reason": "quota"}
    if load_test_running and not mixed:
        return {"decision": "queue", "reason": "acceptance_load_running"}
    return {"decision": "start", "mixed": mixed}
