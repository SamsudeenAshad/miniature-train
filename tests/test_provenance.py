"""Provenance tests (FR-012 slice)."""

from ml.provenance import build_record


def test_provenance_gates():
    ok = build_record("img:v1", {"pkgs": ["a"]}, "none", "ml-pipeline")
    assert ok["loadable"] is True and len(ok["provenance_digest"]) == 64
    assert build_record("img:v1", {"pkgs": []}, "high", "ml-pipeline")["loadable"] is False
    assert build_record("img:v1", {"pkgs": []}, "none", "anon")["loadable"] is False
