"""Label join tests (FR-017 slice)."""

from ml.labels import join


def test_join_coverage_revision_delay():
    preds = [{"ctx": f"c{i}", "event_time": 1000, "pred": 10} for i in range(4)]
    labels = [
        {"ctx": "c0", "label_time": 2000, "value": 11, "rev": 1},
        {"ctx": "c1", "label_time": 3000, "value": 12, "rev": 1},
        {"ctx": "c1", "label_time": 3100, "value": 13, "rev": 2},
    ]
    r = join(preds, labels)
    assert r["joined"] == 2
    assert r["coverage"] == 0.5
    assert r["revisions"] == [1, 2]
    assert r["median_delay_s"] in (1000, 2100)
