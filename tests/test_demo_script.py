"""Demo script tests (Step 44, SRS 19.3 slice)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_demo_covers_all_steps():
    doc = (ROOT / "docs/demo-script.md").read_text()
    for keyword in ("shadow", "canary", "hypotheses", "recovery", "retraining", "export"):
        assert keyword in doc.lower()
