"""Backup/restore reconcile (FR-036, NFR-007 slice)."""

from __future__ import annotations


def reconcile_restore(metadata_digest: str, object_digest: str, release_ref: str, active_refs: set[str]) -> dict:
    reasons = []
    if metadata_digest != object_digest:
        reasons.append("digest_mismatch")
    if release_ref not in active_refs:
        reasons.append("release_ref_orphaned")
    return {"consistent": not reasons, "reasons": reasons}
