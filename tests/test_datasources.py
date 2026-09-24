"""Grafana datasource tests (Step 69)."""

from pathlib import Path

import yaml

K8S = Path(__file__).resolve().parents[1] / "infra/k8s"


def _services():
    svcs = {}
    for f in K8S.glob("*.yaml"):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") == "Service":
                svcs[d["metadata"]["name"]] = d
    return svcs


def test_datasources_point_at_services():
    cm = yaml.safe_load((K8S / "grafana-datasources.yaml").read_text())
    inner = yaml.safe_load(cm["data"]["datasources.yaml"])
    svcs = _services()
    for ds in inner["datasources"]:
        host = ds["url"].split("//")[1].split(":")[0]
        assert host in svcs, f"datasource {ds['name']} points at missing service {host}"
