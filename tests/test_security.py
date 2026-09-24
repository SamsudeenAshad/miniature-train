"""Security control tests (FR-003, NFR-008 slice)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sec = _load("security", "services/control-api/security.py")


def test_ssrf_blocked_and_no_secret_leak():
    bad = sec.check_connector("https://evil.example/data", "s3cr3t")
    assert bad["ok"] is False
    assert "s3cr3t" not in str(bad)
    ok = sec.check_connector("https://objects.internal/bucket/data", "s3cr3t")
    assert ok["ok"] is True
    assert ok["secret_exposed"] is False
    assert "s3cr3t" not in str(ok)
