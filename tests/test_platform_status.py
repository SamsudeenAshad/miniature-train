"""Status ledger tests (Step 100). Ledger must name every unproven area."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ledger_honest():
    doc = (ROOT / "docs/platform-status.md").read_text()
    for keyword in ("unproven", "spof", "sqlite", "untested", "30-day", "in memory"):
        assert keyword in doc.lower(), keyword
