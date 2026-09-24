"""Tempo trace tests (Step 67)."""

from pathlib import Path

import yaml

K8S = Path(__file__).resolve().parents[1] / "infra/k8s"
TEL = Path(__file__).resolve().parents[1] / "infra/telemetry"


def test_traces_pipeline_end_to_end():
    cfg = yaml.safe_load((TEL / "otel-collector.yaml").read_text())
    assert "traces" in cfg["service"]["pipelines"]
    assert "otlp/tempo" in cfg["exporters"]
    docs = list(yaml.safe_load_all((K8S / "tempo.yaml").read_text()))
    svc = next(d for d in docs if d["kind"] == "Service")
    assert svc["metadata"]["name"] == "tempo"
    sts = next(d for d in docs if d["kind"] == "StatefulSet")
    spec = sts["spec"]["template"]["spec"]
    mounted = {v["name"] for v in spec["containers"][0].get("volumeMounts", [])}
    assert {"config", "data"} <= mounted
    assert "config" in {v["name"] for v in spec["volumes"]}
