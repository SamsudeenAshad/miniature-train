"""Append-only audit with digest chain + checkpoint (FR-035 slice)."""

from __future__ import annotations

import hashlib
import json
import time

_log: list[dict] = []


def reset() -> None:
    _log.clear()


def append(actor: str, project: str, action: str, obj: str, outcome: str, policy: str = "v1") -> dict:
    prev = _log[-1]["digest"] if _log else "genesis"
    evt = {
        "actor": actor, "project": project, "action": action, "object": obj,
        "outcome": outcome, "policy_version": policy,
        "correlation_id": f"corr_{len(_log)}", "ts": time.time(), "prev": prev,
    }
    evt["digest"] = hashlib.sha256(json.dumps(evt, sort_keys=True, default=str).encode()).hexdigest()
    _log.append(evt)
    return evt


def verify() -> dict:
    prev = "genesis"
    for e in _log:
        if e["prev"] != prev:
            return {"ok": False, "at": e["correlation_id"]}
        body = {k: v for k, v in e.items() if k != "digest"}
        if hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest() != e["digest"]:
            return {"ok": False, "at": e["correlation_id"]}
        prev = e["digest"]
    return {"ok": True, "events": len(_log), "head": prev}


def checkpoint() -> dict:
    v = verify()
    return {"head": v.get("head"), "events": v.get("events", 0), "ok": v["ok"]}
