"""Alertmanager deploy tests (Step 68)."""

from pathlib import Path

import yaml

K8S = Path(__file__).resolve().parents[1] / "infra/k8s"
TEL = Path(__file__).resolve().parents[1] / "infra/telemetry"


def test_alertmanager_wiring():
    docs = list(yaml.safe_load_all((K8S / "alertmanager.yaml").read_text()))
    kinds = {d["kind"] for d in docs}
    assert {"Deployment", "ConfigMap", "Service"} <= kinds
    dep = next(d for d in docs if d["kind"] == "Deployment")
    assert dep["spec"]["template"]["spec"]["containers"][0]["image"] == "prom/alertmanager:v0.27.0"
    cfg = yaml.safe_load((TEL / "alertmanager.yaml").read_text())
    assert cfg["route"]["receiver"] == "platform"
    cm = next(d for d in docs if d["kind"] == "ConfigMap")
    embedded = yaml.safe_load(cm["data"]["alertmanager.yaml"])
    assert embedded["route"]["receiver"] == cfg["route"]["receiver"]
