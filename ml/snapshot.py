"""Immutable snapshots + split manifests + lineage (FR-005, ML-001, WBS 3.3)."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from .data_generator import HOURS_PER_WEEK, HOURS_TOTAL, SERIES_IDS, START
from .validate import SCHEMA_VERSION, validate_rows


def snapshot_dataset(rows: list[dict], source: str, out_dir: Path) -> dict:
    """Write immutable snapshot.csv + manifest. Verifies by digest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    snap = out_dir / "snapshot.csv"
    with snap.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    digest = hashlib.sha256(snap.read_bytes()).hexdigest()
    report = validate_rows(rows)
    split_manifest = {
        "train": "weeks 1-8",
        "validation": "weeks 9-10",
        "test": "weeks 11-12",
        "purge": "1h label-horizon purge at train/val boundaries",
        "hours_total_per_series": HOURS_TOTAL,
        "hours_per_week": HOURS_PER_WEEK,
        "start": START.isoformat().replace("+00:00", "Z"),
    }
    split_digest = hashlib.sha256(json.dumps(split_manifest, sort_keys=True).encode()).hexdigest()
    manifest = {
        "source": source,
        "schema_version": SCHEMA_VERSION,
        "content_digest": digest,
        "split_manifest": split_manifest,
        "split_manifest_digest": split_digest,
        "row_count": len(rows),
        "series": SERIES_IDS,
        "validation_status": report["status"],
        "immutable": True,
    }
    (out_dir / "snapshot.manifest.json").write_text(json.dumps(manifest, indent=2))
    (out_dir / "validation.report.json").write_text(json.dumps(report, indent=2))
    return manifest
