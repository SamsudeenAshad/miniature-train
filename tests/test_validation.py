"""Validation/quarantine tests (FR-004)."""

from ml.data_generator import generate_rows
from ml.validate import validate_rows


def test_valid_fixture_accepted():
    rows = generate_rows(seed=42)[:500]
    rep = validate_rows(rows)
    assert rep["status"] == "accepted"
    assert rep["finding_count"] == 0


def test_duplicate_key_quarantined():
    rows = generate_rows(seed=42)[:100]
    rows = rows + [dict(rows[0])]
    rep = validate_rows(rows)
    assert rep["status"] == "quarantined"
    assert any(f["rule"] == "duplicate_key" for f in rep["findings"])


def test_future_leak_quarantined():
    rows = generate_rows(seed=42)[:10]
    bad = dict(rows[0])
    bad["promotion_known_at"] = "2099-01-01T00:00:00Z"
    rep = validate_rows([bad])
    assert rep["status"] == "quarantined"
    assert any(f["rule"] == "future_leak" for f in rep["findings"])


def test_negative_orders_quarantined():
    rows = generate_rows(seed=42)[:5]
    bad = dict(rows[0])
    bad["orders"] = -3
    rep = validate_rows([bad])
    assert rep["status"] == "quarantined"
