"""Fault/load harness seeder (WBS 7.1 slice). Ground truth kept separate from features."""

from __future__ import annotations

import hashlib
import json

FAMILIES = ("cpu", "memory", "latency", "errors", "faulty_deploy")
FAULT_MIN_S = 300
FAULT_MAX_S = 600
RECOVERY_MIN_S = 600


def plan_episodes(seed: int, per_family: int = 6) -> dict:
    episodes, t = [], 0
    for fam in FAMILIES:
        for i in range(per_family):
            dur = FAULT_MIN_S + (seed + i * 37) % (FAULT_MAX_S - FAULT_MIN_S)
            episodes.append({"id": f"{fam}-{i}", "family": fam, "start": t, "end": t + dur, "seed": seed + i})
            t += dur + RECOVERY_MIN_S
    frozen = hashlib.sha256(json.dumps(episodes, sort_keys=True).encode()).hexdigest()
    return {"episodes": episodes, "frozen_digest": frozen, "ground_truth_store": "protected:not_in_features"}
