"""CLI stage tests (Step 245). dvc.yaml commands resolve to working entry points."""

import json

from ml.data_generator import write_dataset
from ml.snapshot_cli import main as snapshot_main
from ml.validate_cli import main as validate_main


def test_cli_stages_end_to_end(tmp_path):
    write_dataset(42, tmp_path / "demand.csv", tmp_path / "manifest.json")
    rep = validate_main(["--in", str(tmp_path / "demand.csv"), "--out", str(tmp_path / "report.json")])
    assert rep["status"] == "accepted"
    manifest = snapshot_main(["--in", str(tmp_path / "demand.csv"), "--out", str(tmp_path / "snap")])
    assert manifest["immutable"] is True
    assert json.loads((tmp_path / "report.json").read_text())["status"] == "accepted"
