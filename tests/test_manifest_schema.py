"""Manifest conformance tests (Step 197). Generator manifests match the published schema."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generator_manifest_conforms(tmp_path):
    from ml.data_generator import write_dataset

    schema = json.loads((ROOT / "packages/contracts/schemas/dataset-manifest.schema.json").read_text())
    manifest = write_dataset(42, tmp_path / "demand.csv", tmp_path / "manifest.json")
    for key in schema["required"]:
        assert key in manifest, key
    assert manifest["rows"] == 20160


def test_snapshot_manifest_conforms(tmp_path):
    from ml.data_generator import generate_rows
    from ml.snapshot import snapshot_dataset

    schema = json.loads((ROOT / "packages/contracts/schemas/snapshot-manifest.schema.json").read_text())
    manifest = snapshot_dataset(generate_rows(seed=42)[:500], source="test", out_dir=tmp_path)
    for key in schema["required"]:
        assert key in manifest, key
    assert manifest["immutable"] is True
