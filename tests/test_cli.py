"""CLI stage tests (Step 245). dvc.yaml commands resolve to working entry points."""

import json
import subprocess
import sys
from pathlib import Path

from ml.data_generator import write_dataset
from ml.snapshot_cli import main as snapshot_main
from ml.validate_cli import main as validate_main

ROOT = Path(__file__).resolve().parents[1]


def test_cli_stages_end_to_end(tmp_path):
    write_dataset(42, tmp_path / "demand.csv", tmp_path / "manifest.json")
    rep = validate_main(["--in", str(tmp_path / "demand.csv"), "--out", str(tmp_path / "report.json")])
    assert rep["status"] == "accepted"
    manifest = snapshot_main(["--in", str(tmp_path / "demand.csv"), "--out", str(tmp_path / "snap")])
    assert manifest["immutable"] is True
    assert json.loads((tmp_path / "report.json").read_text())["status"] == "accepted"


def test_module_invocations_match_dvc(tmp_path):
    write_dataset(42, tmp_path / "demand.csv", tmp_path / "manifest.json")
    for mod, args in (("ml.validate_cli", ["--in", str(tmp_path / "demand.csv"),
                                           "--out", str(tmp_path / "r.json")]),
                      ("ml.snapshot_cli", ["--in", str(tmp_path / "demand.csv"),
                                           "--out", str(tmp_path / "s")])):
        proc = subprocess.run([sys.executable, "-m", mod, *args],
                              capture_output=True, text=True, cwd=ROOT)
        assert proc.returncode == 0, proc.stderr
