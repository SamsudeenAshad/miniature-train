"""Telemetry deploy tests (Step 56)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_prometheus_grafana_pinned():
    docs = list(yaml.safe_load_all((ROOT / "telemetry.yaml").read_text()))
    images = [c["image"] for d in docs if d["kind"] == "Deployment" for c in d["spec"]["template"]["spec"]["containers"]]
    assert "prom/prometheus:v2.53.0" in images
    assert "grafana/grafana:11.3.0" in images
