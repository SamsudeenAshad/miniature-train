"""Fault benchmark + event scoring (ML-004/005, AT-13/14 slice, WBS 7.1/10.2).

Partitions: dev faults (>=60), held-out 30 (6 each: cpu, memory,
latency, errors, faulty_deploy), healthy >=24h. Match: correct
service group, raised in [start, end+180s], one-to-one. Delays on
detected only; misses separate. Top-k frozen at detection+5min;
abstentions count as misses.
"""

from __future__ import annotations

import statistics

from workers.aiops.harness import FAMILIES as FAULT_FAMILIES

MATCH_GRACE_S = 180


def match(incidents: list[dict], episodes: list[dict]) -> dict:
    used: set[int] = set()
    tp, delays = 0, []
    for ep in episodes:
        hit = None
        for i, inc in enumerate(incidents):
            if i in used:
                continue
            if inc["service_group"] != ep["service_group"]:
                continue
            if ep["start"] <= inc["ts"] <= ep["end"] + MATCH_GRACE_S:
                hit = i
                break
        if hit is not None:
            used.add(hit)
            tp += 1
            delays.append(incidents[hit]["ts"] - next(e["start"] for e in episodes if e["id"] == ep["id"]))
    fp = len(incidents) - len(used)
    fn = len(episodes) - tp
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    delays_sorted = sorted(delays)
    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "tp": tp, "fp": fp, "fn": fn,
        "delay_median_s": statistics.median(delays_sorted) if delays_sorted else None,
        "delay_p95_s": sorted(delays_sorted)[max(0, int(0.95 * len(delays_sorted)) - 1)] if delays_sorted else None,
    }


def diagnosis_score(predictions: list[dict], eligible: int) -> dict:
    """predictions: [{episode_id, rank1, rank2, rank3, truth, abstained}]."""
    top1 = sum(1 for p in predictions if not p.get("abstained") and p["rank1"] == p["truth"])
    top3 = sum(1 for p in predictions if not p.get("abstained") and p["truth"] in (p["rank1"], p["rank2"], p["rank3"]))
    return {
        "top1": round(top1 / eligible, 3) if eligible else 0.0,
        "top3": round(top3 / eligible, 3) if eligible else 0.0,
        "eligible": eligible,
    }
