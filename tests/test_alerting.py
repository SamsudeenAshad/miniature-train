"""Alerting config tests (Step 32, FR-020 slice)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/telemetry"


def test_rules_and_routing():
    rules = yaml.safe_load((ROOT / "prometheus-rules.yaml").read_text())
    names = {r["alert"] for g in rules["groups"] for r in g["rules"]}
    assert {"HighErrorRate", "SevereErrorRate", "HighLatency", "TelemetryStale"} <= names
    am = yaml.safe_load((ROOT / "alertmanager.yaml").read_text())
    assert "service" in am["route"]["group_by"]
    assert am["inhibit_rules"][0]["equal"] == ["service", "environment"]
