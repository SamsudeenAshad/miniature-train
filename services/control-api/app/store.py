"""Storage seam (Step 152). Routes depend on this interface, not on memory.

A Postgres implementation can replace MemoryStore without touching routes.
Tables: 001_projects, 002_idempotency.
"""

from __future__ import annotations


class MemoryStore:
    backend = "memory"

    def __init__(self) -> None:
        self.projects: dict[str, dict] = {}
        self.members: dict[str, dict[str, str]] = {}
        self.idem: dict[str, dict] = {}

    def reset(self) -> None:
        self.projects.clear()
        self.members.clear()
        self.idem.clear()
