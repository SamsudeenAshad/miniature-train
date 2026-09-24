"""Dashboard provisioning tests (Step 86). Mounts match the ConfigMap; JSON mirrors source."""

import json
from pathlib import Path

import yaml

K8S = Path(__file__).resolve().parents[1] / "infra/k8s"
TEL = Path(__file__).resolve().parents[1] / "infra/telemetry"


def test_dashboard_provisioned():
    cm = yaml.safe_load((K8S / "grafana-dashboards.yaml").read_text())
    assert set(cm["data"]) == {"provider.yaml", "operations.json"}
    assert json.loads(cm["data"]["operations.json"]) == json.loads((TEL / "dashboard.json").read_text())
    grafana = next(d for d in yaml.safe_load_all((K8S / "telemetry.yaml").read_text())
                   if d.get("kind") == "Deployment" and d["metadata"]["name"] == "grafana")
    spec = grafana["spec"]["template"]["spec"]
    mounted = {v["name"] for v in spec["containers"][0]["volumeMounts"]}
    provided = {v["name"] for v in spec["volumes"]}
    assert {"dashboards", "provisioning"} <= mounted & provided
