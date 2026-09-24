"""Backup/restore reconcile (FR-036, NFR-007 slice)."""

from __future__ import annotations

import argparse
import json


def reconcile_restore(metadata_digest: str, object_digest: str, release_ref: str, active_refs: set[str]) -> dict:
    reasons = []
    if metadata_digest != object_digest:
        reasons.append("digest_mismatch")
    if release_ref not in active_refs:
        reasons.append("release_ref_orphaned")
    return {"consistent": not reasons, "reasons": reasons}


def main(argv: list[str] | None = None) -> dict:
    ap = argparse.ArgumentParser(description="Nightly backup job")
    ap.add_argument("--rpo-hours", type=int, default=24)
    ap.add_argument("--retain", type=int, default=30)
    args = ap.parse_args(argv)
    plan = {"rpo_hours": args.rpo_hours, "retain": args.retain, "targets": ["metadata", "objects"]}
    print(json.dumps(plan))
    return plan


if __name__ == "__main__":
    main()
