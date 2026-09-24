"""Artifact trust policy (FR-012 slice, WBS 4.4)."""

from __future__ import annotations

TRUSTED_SIGNERS = ("ml-pipeline",)


def verify_artifact(digest: str, signature: str, signer: str, vuln_severity: str) -> dict:
    if signer not in TRUSTED_SIGNERS:
        return {"load": False, "reason": "untrusted_signer"}
    if not signature or not digest:
        return {"load": False, "reason": "missing_signature_or_digest"}
    if vuln_severity in ("critical", "high"):
        return {"load": False, "reason": f"unresolved_{vuln_severity}"}
    return {"load": True, "reason": "ok"}
