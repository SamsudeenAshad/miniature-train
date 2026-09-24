"""Training job lifecycle (FR-007 slice, WBS 4.1).

States: queued/running/succeeded/failed/cancelled/timed-out.
One logical run + attempt history; bounded retries; cancellation and
timeout preserve attempts; crash recovery requeues without duplicating
the logical run.
"""

from __future__ import annotations

TERMINAL = ("succeeded", "failed", "cancelled", "timed-out")
MAX_ATTEMPTS = 3


def submit(run_id: str, idempotency: dict, key: str) -> dict:
    if key in idempotency:
        return idempotency[key]
    run = {"run_id": run_id, "state": "queued", "attempts": [], "cancel_requested": False}
    idempotency[key] = run
    return run


def start_attempt(run: dict, attempt: int) -> dict:
    if run["state"] in TERMINAL:
        raise ValueError("already_terminal")
    if len(run["attempts"]) >= MAX_ATTEMPTS:
        raise ValueError("retry_budget_exhausted")
    run = dict(run, state="running", attempts=run["attempts"] + [{"attempt": attempt, "result": "started"}])
    return run


def finish(run: dict, result: str) -> dict:
    if result not in ("succeeded", "failed", "timed-out"):
        raise ValueError("bad_result")
    attempts = run["attempts"][:-1] + [dict(run["attempts"][-1], result=result)]
    return dict(run, state=result, attempts=attempts)


def cancel(run: dict) -> dict:
    if run["state"] in TERMINAL:
        raise ValueError("already_terminal")
    return dict(run, state="cancelled", cancel_requested=True)


def recover(run: dict) -> dict:
    """Worker crash: running goes back to queued, attempt kept as crashed."""
    if run["state"] != "running":
        return run
    attempts = run["attempts"][:-1] + [dict(run["attempts"][-1], result="crashed")]
    return dict(run, state="queued", attempts=attempts)
