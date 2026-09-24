"""Time-aware topology (FR-024 slice, WBS 7.3). Edges carry provenance/expiry."""

from __future__ import annotations

TTL_S = 3600


def update(edges: dict[tuple, dict], src: str, dst: str, evidence: str, now: float) -> dict:
    edges[(src, dst)] = {"evidence": evidence, "last_seen": now, "expires": now + TTL_S}
    return edges


def neighbors(edges: dict[tuple, dict], svc: str, now: float) -> list[str]:
    out = []
    for (s, d), meta in edges.items():
        if meta["expires"] < now:
            continue
        if s == svc:
            out.append(d)
        elif d == svc:
            out.append(s)
    return sorted(out)
