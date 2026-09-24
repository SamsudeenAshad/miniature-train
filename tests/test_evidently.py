"""Evidently adapter tests (Step 36)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "workers/aiops"


def test_adapter_thresholds():
    cfg = yaml.safe_load((ROOT / "evidently.yaml").read_text())
    assert cfg["window"]["min_observations"] == 500
    assert cfg["thresholds"]["mean_shift"] == 0.15
    assert cfg["missingness"]["rule"] == "separate"
