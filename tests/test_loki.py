"""Loki deploy tests (Step 66)."""

from pathlib import Path

import yaml

K8S = Path(__file__).resolve().parents[1] / "infra/k8s"
TEL = Path(__file__).resolve().parents[1] / "infra/telemetry"


def test_loki_matches_collector_exporter():
    docs = list(yaml.safe_load_all((K8S / "loki.yaml").read_text()))
    svc = next(d for d in docs if d["kind"] == "Service")
    assert svc["metadata"]["name"] == "loki"
    assert any(p["port"] == 3100 for p in svc["spec"]["ports"])
    cfg = yaml.safe_load((TEL / "otel-collector.yaml").read_text())
    assert "loki" in cfg["exporters"]
