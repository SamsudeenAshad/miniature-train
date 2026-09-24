"""Dashboard tests (Step 58)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "infra/telemetry"


def test_dashboard_panels():
    dash = json.loads((ROOT / "dashboard.json").read_text())
    titles = {p["title"] for p in dash["panels"]}
    assert {"p95 latency", "5xx rate", "telemetry freshness", "canary weight"} <= titles
