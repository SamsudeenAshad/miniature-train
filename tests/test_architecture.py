"""Architecture pack tests (Step 46)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_architecture_sections():
    doc = (ROOT / "docs/architecture.md").read_text()
    for h in ("Responsibilities", "Trust boundaries", "ADRs", "Data flow"):
        assert h in doc
