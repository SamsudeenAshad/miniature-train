"""Acceptance decision tests (Step 49, SRS 14.4 slice)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_slo_labelled_pending():
    doc = (ROOT / "docs/acceptance-decisions.md").read_text()
    assert "pending" in doc.lower()
    assert "R3" in doc
