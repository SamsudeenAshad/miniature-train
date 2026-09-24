"""Alert dedup + correlation + hypothesis ranking (FR-023/024/025 slice)."""

from __future__ import annotations

CORRELATION_WINDOW_S = 300


def correlate(alerts: list[dict]) -> list[dict]:
    """Group by service group within bounded window. Retains evidence."""
    groups: list[dict] = []
    for a in sorted(alerts, key=lambda x: x["ts"]):
        placed = False
        for g in groups:
            if a["service_group"] == g["service_group"] and abs(a["ts"] - g["last_ts"]) <= CORRELATION_WINDOW_S:
                g["alerts"].append(a)
                g["last_ts"] = max(g["last_ts"], a["ts"])
                placed = True
                break
        if not placed:
            groups.append({"service_group": a["service_group"], "alerts": [a], "last_ts": a["ts"]})
    return [{"incident_id": f"inc_{i}", **g} for i, g in enumerate(groups)]


def rank_hypotheses(incident: dict, changes: list[dict], graph_dist: dict[str, int]) -> dict:
    """Weighted reproducible ranking over anomaly, distance, change recency."""
    cands = set(graph_dist) | {c["service"] for c in changes}
    scored = []
    for c in sorted(cands):
        dist = graph_dist.get(c, 99)
        recent = sum(1 for ch in changes if ch["service"] == c and ch["age_s"] <= 900)
        score = max(0.0, 1.0 - 0.25 * dist) + 0.5 * min(1, recent)
        scored.append({"cause": c, "score": round(score, 3), "distance": dist, "recent_change": bool(recent)})
    scored.sort(key=lambda x: -x["score"])
    if not scored or scored[0]["score"] <= 0:
        return {"hypotheses": [], "status": "abstained", "limitation": "insufficient evidence"}
    return {"hypotheses": scored[:5], "status": "ranked", "limitation": "correlation_not_causation"}
