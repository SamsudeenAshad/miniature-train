"""Runner stage tests (Step 77, FR-007 slice)."""

import json
import subprocess
import sys
from pathlib import Path

from workers.training.runner import main, run_stage

ROOT = Path(__file__).resolve().parents[1]


def test_all_stages():
    assert run_stage("validate")["status"] == "accepted"
    assert len(run_stage("train")["artifact_digest"]) == 64
    assert "mae" in run_stage("evaluate")
    assert run_stage("register")["version"] == 1
    assert main(["--stage", "validate"])["status"] == "accepted"


def test_module_invocation_matches_workflow():
    proc = subprocess.run([sys.executable, "-m", "workers.training.runner",
                           "--stage", "validate"],
                          capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["status"] == "accepted"
