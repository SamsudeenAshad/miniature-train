"""Model card tests (Step 45)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs/model-cards"


def test_cards_have_lineage_and_limits():
    fore = (ROOT / "demand-forecaster.md").read_text()
    assert "Lineage" in fore and "Limits" in fore
    det = (ROOT / "anomaly-detector.md").read_text()
    assert "not a probability" in det and "Challenger" in det
