"""Connector + secret hardening (FR-003, NFR-008 slice, AT-24)."""

from __future__ import annotations

from urllib.parse import urlparse

ALLOWED_HOSTS = ("objects.internal", "telemetry.internal")


def check_connector(url: str, secret_value: str | None) -> dict:
    """Reject arbitrary fetch; never echo secrets in diagnostics."""
    try:
        host = urlparse(url).hostname or ""
    except Exception:
        return {"ok": False, "diagnostic": "malformed_url"}
    if host not in ALLOWED_HOSTS:
        return {"ok": False, "diagnostic": f"host_not_allowlisted:{host}"}
    if secret_value:
        return {"ok": True, "secret_ref": "ref:connector-secret", "secret_exposed": False}
    return {"ok": True, "secret_ref": None, "secret_exposed": False}
