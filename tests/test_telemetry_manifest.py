"""Telemetry manifest tests (Step 31)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/telemetry"


def test_collector_redacts_and_exports():
    cfg = yaml.safe_load((ROOT / "otel-collector.yaml").read_text())
    actions = cfg["processors"]["attributes"]["actions"]
    deleted = {a["key"] for a in actions if a["action"] == "delete"}
    assert {"authorization", "cookie"} <= deleted
    assert "prometheus" in cfg["exporters"]
