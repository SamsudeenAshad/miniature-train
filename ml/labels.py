"""Delayed labels join (FR-017 slice, WBS 6.4).

Predictions keyed by project-scoped (series_id, target_time, model_version)
contexts. Duplicate/revised labels versioned; quality reports state
coverage, arrival delay, window, and revision.
"""

from __future__ import annotations


def join(predictions: list[dict], labels: list[dict]) -> dict:
    """Each prediction: {ctx, event_time}. Each label: {ctx, label_time, value, rev}."""
    latest: dict[str, dict] = {}
    for lb in labels:
        cur = latest.get(lb["ctx"])
        if cur is None or lb["rev"] > cur["rev"]:
            latest[lb["ctx"]] = lb
    joined, delays = [], []
    for p in predictions:
        lb = latest.get(p["ctx"])
        if lb is None:
            continue
        joined.append({"ctx": p["ctx"], "pred": p.get("pred"), "label": lb["value"], "rev": lb["rev"]})
        delays.append(lb["label_time"] - p["event_time"])
    coverage = len(joined) / len(predictions) if predictions else 0.0
    return {
        "joined": len(joined),
        "coverage": round(coverage, 3),
        "median_delay_s": sorted(delays)[len(delays) // 2] if delays else None,
        "revisions": sorted({j["rev"] for j in joined}),
        "rows": joined,
    }
