"""ServiceMonitor tests (Step 65)."""

from pathlib import Path

import yaml

K8S = Path(__file__).resolve().parents[1] / "infra/k8s"
TEL = Path(__file__).resolve().parents[1] / "infra/telemetry"


def _all_docs(path: Path):
    return list(yaml.safe_load_all(path.read_text()))


def test_monitors_match_named_ports():
    monitors = _all_docs(TEL / "servicemonitors.yaml")
    assert {m["metadata"]["name"] for m in monitors} == {"control-api", "inference"}
    services = {}
    for f in ("service.yaml", "inference.yaml"):
        for d in _all_docs(K8S / f):
            if d["kind"] == "Service":
                services[d["metadata"]["name"]] = d
    for m in monitors:
        target = m["metadata"]["name"]
        ports = {p.get("name") for p in services[target]["spec"]["ports"]}
        for ep in m["spec"]["endpoints"]:
            assert ep["port"] in ports, f"{target} missing named port {ep['port']}"
