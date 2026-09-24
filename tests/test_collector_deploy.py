"""Collector deploy tests (Step 57)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_collector_wiring():
    docs = list(yaml.safe_load_all((ROOT / "collector.yaml").read_text()))
    kinds = {d["kind"] for d in docs}
    assert {"Deployment", "ConfigMap", "Service"} <= kinds
    dep = next(d for d in docs if d["kind"] == "Deployment")
    img = dep["spec"]["template"]["spec"]["containers"][0]["image"]
    assert img == "otel/opentelemetry-collector-contrib:0.103.0"
