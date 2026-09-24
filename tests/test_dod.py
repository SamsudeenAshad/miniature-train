"""DoD tracker tests (Step 48, SRS 19.1 slice)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dod_items_present_and_honest():
    doc = (ROOT / "docs/definition-of-done.md").read_text()
    assert doc.count("- [ ]") >= 13
    assert "- [x]" not in doc.lower()
