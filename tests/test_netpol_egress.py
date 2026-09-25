"""NetworkPolicy egress tests (Step 106). Every Service port must be reachable in-namespace."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _services():
    ports = set()
    for f in ROOT.glob("*.yaml"):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") == "Service":
                for p in d["spec"]["ports"]:
                    ports.add(p["port"])
    return ports


def test_egress_covers_services():
    np = yaml.safe_load((ROOT / "networkpolicy.yaml").read_text())
    allowed = {p["port"] for e in np["spec"]["egress"] for p in e.get("ports", [])}
    needed = _services()
    assert needed <= allowed, needed - allowed
