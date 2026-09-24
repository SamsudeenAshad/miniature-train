"""Governance tests (FR-001/035/036, NFR-007/009 slice)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_authz = _load("authz", ROOT / "services/control-api/authz.py")
_audit = _load("audit", ROOT / "services/control-api/audit.py")
_restore = _load("restore", ROOT / "infra/restore.py")


def test_cross_project_denied_and_self_approval():
    assert _authz.can("ml_engineer", "submit_run", "p1", "p1") is True
    assert _authz.can("ml_engineer", "submit_run", "p1", "p2") is False
    assert _authz.can("viewer", "submit_run", "p1", "p1") is False
    assert _authz.can_approve("project_admin", "a", "a") is False
    assert _authz.can_approve("project_admin", "a", "b") is True


def test_audit_append_only_and_tamper_evident():
    _audit.reset()
    _audit.append("u1", "p1", "approve_release", "rel-1", "allow")
    _audit.append("u2", "p1", "promote", "rel-1", "deny")
    v = _audit.verify()
    assert v["ok"] is True and v["events"] == 2
    cp = _audit.checkpoint()
    assert cp["ok"] is True
    _audit._log[0]["outcome"] = "allow-tampered"
    assert _audit.verify()["ok"] is False


def test_restore_reconcile():
    ok = _restore.reconcile_restore("d1", "d1", "rel-1", {"rel-1"})
    assert ok["consistent"] is True
    bad = _restore.reconcile_restore("d1", "d2", "rel-9", {"rel-1"})
    assert bad["consistent"] is False
