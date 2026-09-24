"""Transactional outbox + at-least-once consumer dedup (ADR-02, SRS 10.4 slice)."""

from __future__ import annotations

import time
import uuid

_outbox: list[dict] = []
_seen: set[str] = set()


def reset() -> None:
    _outbox.clear()
    _seen.clear()


def publish(event_type: str, project: str, payload: dict, environment: str = "staging") -> dict:
    evt = {
        "schema_version": "1.0",
        "event_id": f"evt_{uuid.uuid4().hex[:12]}",
        "event_type": event_type,
        "project_id": project,
        "environment": environment,
        "occurred_at": time.time(),
        "ingested_at": time.time(),
        "correlation_id": f"corr_{len(_outbox)}",
        "payload": payload,
        "delivered": False,
    }
    _outbox.append(evt)  # same-transaction with state change (simulated)
    return evt


def consume(evt: dict) -> dict:
    if evt["event_id"] in _seen:
        return {"deduped": True}
    _seen.add(evt["event_id"])
    return {"deduped": False, "event_id": evt["event_id"]}
