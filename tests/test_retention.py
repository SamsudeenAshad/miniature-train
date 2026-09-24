"""Retention tests (FR-036 slice)."""

from infra.retention import after_restore, request_delete, reset


def test_active_ref_and_hold_block():
    reset()
    assert request_delete("m1", {"m1"})["deleted"] is False
    assert request_delete("m2", set(), hold={"owner": "o", "expired": False})["reason"] == "retention_hold"
    assert request_delete("m2", set())["deleted"] is True
    assert after_restore(["m2", "m3"]) == {"reapplied": ["m2"]}
