"""Migration ordering (Step 142). Pure apply-order logic; the live runner comes with a DB."""

from __future__ import annotations

from pathlib import Path


def pending(migrations_dir: Path, applied: set[str]) -> list[Path]:
    files = sorted(migrations_dir.glob("*.sql"))
    return [f for f in files if f.name not in applied]
