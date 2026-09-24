"""Canary rollout policy (SRS 11.3, FR-014 slice, WBS 5.3).

Stages 5/25/50/100%. First three need >=5 min and >=1000 candidate
requests. Each 1-min interval needs >=100 requests. Fail: 5xx>1% or
+0.5pp vs stable or p95>200ms. Abort on 3 consecutive fails; severe
guard 5xx>5% (>=100 req) aborts in one interval. Insufficient evidence
pauses; 30 min without evidence requires review.
"""

from __future__ import annotations

STAGES = (5, 25, 50, 100)
MIN_STAGE_MIN = 5
MIN_STAGE_REQUESTS = 1000
MIN_INTERVAL_REQUESTS = 100
P95_LIMIT_MS = 200.0
ERR_LIMIT = 0.01
ERR_DELTA_LIMIT = 0.005
SEVERE_ERR = 0.05
NO_EVIDENCE_REVIEW_MIN = 30


def eval_interval(candidate_5xx: int, candidate_n: int, stable_5xx_rate: float, p95_ms: float) -> dict:
    if candidate_n < MIN_INTERVAL_REQUESTS:
        return {"verdict": "insufficient", "reason": "low_volume"}
    err = candidate_5xx / candidate_n
    if err > SEVERE_ERR:
        return {"verdict": "abort", "reason": "severe_errors"}
    if err > ERR_LIMIT or (err - stable_5xx_rate) > ERR_DELTA_LIMIT or p95_ms > P95_LIMIT_MS:
        return {"verdict": "fail", "reason": "guard_failed"}
    return {"verdict": "pass", "reason": "ok"}


def advance(stage: int, minutes: int, requests: int, consecutive_fails: int, no_evidence_min: int) -> dict:
    if no_evidence_min >= NO_EVIDENCE_REVIEW_MIN:
        return {"action": "review", "reason": "no_evidence_30min"}
    if consecutive_fails >= 3:
        return {"action": "abort", "reason": "three_fails"}
    if stage not in STAGES:
        return {"action": "hold", "reason": "unknown_stage"}
    if stage == 100:
        return {"action": "observe", "reason": "final_observation_10min"}
    if minutes >= MIN_STAGE_MIN and requests >= MIN_STAGE_REQUESTS and consecutive_fails == 0:
        nxt = STAGES[STAGES.index(stage) + 1]
        return {"action": "promote", "next": nxt}
    return {"action": "hold", "reason": "stage_requirements_unmet"}
