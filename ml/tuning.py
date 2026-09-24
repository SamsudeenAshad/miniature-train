"""Bounded tuning search (FR-008 slice, WBS 4.3). Stops at limits, never auto-promotes."""

from __future__ import annotations

import itertools
import random

MAX_TRIALS = 12


def search(space: dict[str, list], seed: int, max_trials: int = MAX_TRIALS) -> dict:
    rng = random.Random(seed)
    keys = sorted(space)
    combos = list(itertools.product(*[space[k] for k in keys]))
    rng.shuffle(combos)
    trials = [{k: v for k, v in zip(keys, c)} for c in combos[:max_trials]]
    return {
        "trials": trials,
        "count": len(trials),
        "seed": seed,
        "strategy": "grid_shuffled",
        "auto_promoted": False,
        "truncated": len(combos) > max_trials,
    }
