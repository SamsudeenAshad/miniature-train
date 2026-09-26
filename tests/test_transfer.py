"""Transfer record tests (Step 47, SRS 19.2 slice)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_transfer_owners():
    doc = (ROOT / "docs/transfer-record.md").read_text()
    for owner in ("platform engineer", "ml engineer", "service owner", "project admin"):
        assert owner in doc
    assert "ExternalSecret" in doc or "externalsecret" in doc.lower()
    for secret in ("control-api", "object-store"):
        assert secret in doc, secret
