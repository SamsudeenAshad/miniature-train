"""Snapshot immutability tests (FR-005, ML-001)."""

import json

from ml.data_generator import generate_rows
from ml.snapshot import snapshot_dataset


def test_snapshot_manifest_and_digests(tmp_path):
    rows = generate_rows(seed=42)[:1000]
    m = snapshot_dataset(rows, source="synthetic:demand-gen-0.1.0", out_dir=tmp_path)
    assert m["immutable"] is True
    assert m["validation_status"] == "accepted"
    assert m["row_count"] == 1000
    assert len(m["content_digest"]) == 64
    assert len(m["split_manifest_digest"]) == 64
    on_disk = json.loads((tmp_path / "snapshot.manifest.json").read_text())
    assert on_disk == m


def test_snapshot_repeatable(tmp_path):
    rows = generate_rows(seed=11)[:200]
    m1 = snapshot_dataset(rows, source="s", out_dir=tmp_path / "a")
    m2 = snapshot_dataset(rows, source="s", out_dir=tmp_path / "b")
    assert m1["content_digest"] == m2["content_digest"]
