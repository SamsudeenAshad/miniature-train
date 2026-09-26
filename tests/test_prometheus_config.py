"""Prometheus config tests (Step 87). Rules mirror source; mounts present."""

from pathlib import Path

import yaml

K8S = Path(__file__).resolve().parents[1] / "infra/k8s"
TEL = Path(__file__).resolve().parents[1] / "infra/telemetry"


def _by_name(docs, kind, name):
    return next(d for d in docs if d.get("kind") == kind and d["metadata"]["name"] == name)


def test_rules_mirror_and_mounts():
    src = yaml.safe_load((TEL / "prometheus-rules.yaml").read_text())
    src_names = {r["alert"] for g in src["groups"] for r in g["rules"]}
    cfg_docs = list(yaml.safe_load_all((K8S / "prometheus-config.yaml").read_text()))
    cm = _by_name(cfg_docs, "ConfigMap", "prometheus-rules")
    mirrored = yaml.safe_load(cm["data"]["health.yaml"])
    assert {r["alert"] for g in mirrored["groups"] for r in g["rules"]} == src_names
    prom = _by_name(list(yaml.safe_load_all((K8S / "telemetry.yaml").read_text())), "Deployment", "prometheus")
    spec = prom["spec"]["template"]["spec"]
    assert {"config", "rules"} <= {v["name"] for v in spec["volumes"]}
    cfg = _by_name(cfg_docs, "ConfigMap", "prometheus")
    server = yaml.safe_load(cfg["data"]["prometheus.yaml"])
    assert server["global"]["scrape_interval"] == "30s"
    assert server["global"]["evaluation_interval"] == "30s"
