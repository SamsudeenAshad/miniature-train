"""Fault/load harness seeder (WBS 7.1 slice). Ground truth kept separate from features."""

from __future__ import annotations

import hashlib
import json

FAMILIES = ("cpu", "memory", "latency", "errors", "faulty_deploy")
FAULT_MIN_S = 300
FAULT_MAX_S = 600
RECOVERY_MIN_S = 600


def plan_episodes(seed: int, per_family: int = 6, allowlist: tuple[str, ...] = ()) -> dict:
    """Plan fault episodes. Injection is allowlisted: an empty allowlist plans nothing.

    Only families named in ``allowlist`` receive episodes; anything else must
    never be faulted outside explicitly enrolled test targets (SRS ASM-06).
    """
    if not allowlist:
        raise ValueError("allowlist_empty_no_faults_planned")
    unknown = set(allowlist) - set(FAMILIES)
    if unknown:
        raise ValueError(f"unknown_families:{sorted(unknown)}")
    episodes, t = [], 0
    for fam in FAMILIES:
        if fam not in allowlist:
            continue
        for i in range(per_family):
            dur = FAULT_MIN_S + (seed + i * 37) % (FAULT_MAX_S - FAULT_MIN_S)
            episodes.append({"id": f"{fam}-{i}", "family": fam, "start": t, "end": t + dur, "seed": seed + i})
            t += dur + RECOVERY_MIN_S
    frozen = hashlib.sha256(json.dumps(episodes, sort_keys=True).encode()).hexdigest()
    return {"episodes": episodes, "frozen_digest": frozen, "ground_truth_store": "protected:not_in_features"}
