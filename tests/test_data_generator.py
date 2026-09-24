"""Seeded generator checks (SRS 7.3, ML-001 slice)."""

from ml.data_generator import (
    HOURS_TOTAL,
    SERIES_IDS,
    assign_split,
    generate_rows,
    is_purge_hour,
)


def test_row_count_and_series():
    rows = generate_rows(seed=42)
    assert len(rows) == HOURS_TOTAL * len(SERIES_IDS) == 20160
    assert sorted({r["series_id"] for r in rows}) == sorted(SERIES_IDS)


def test_determinism():
    a = generate_rows(seed=7)
    b = generate_rows(seed=7)
    assert a == b
    c = generate_rows(seed=8)
    assert a != c


def test_splits_time_ordered_and_purge():
    rows = generate_rows(seed=42)
    by_split = {}
    for r in rows:
        by_split[r["split"]] = by_split.get(r["split"], 0) + 1
    # 8/12 train, 2/12 val, 2/12 test per series (purge flagged, not removed)
    per_series = HOURS_TOTAL
    assert by_split["train"] == 10 * per_series * 8 // 12
    assert by_split["validation"] == 10 * per_series * 2 // 12
    assert by_split["test"] == 10 * per_series * 2 // 12
    purged = [r for r in rows if r["purge_excluded"]]
    assert len(purged) == 10 * 2  # last hour of train + val per series
    # purge hours belong to train/val, never test
    assert {r["split"] for r in purged} <= {"train", "validation"}


def test_no_future_leakage_and_ranges():
    rows = generate_rows(seed=42)
    for r in rows:
        assert r["promotion_known_at"] <= r["event_time"]
        assert r["orders"] >= 0
        assert r["split"] in ("train", "validation", "test")
    assert assign_split.__doc__ is not None
    assert is_purge_hour.__doc__ is not None
