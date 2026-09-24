"""Probe tests (Step 96). Telemetry components all expose readiness + liveness."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"
WANT = {"prometheus", "grafana", "otel-collector", "alertmanager", "loki", "tempo",
        "db", "object-store", "mlflow"}


def _deployments():
    for f in sorted(ROOT.glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") in ("Deployment", "StatefulSet"):
                yield d["metadata"]["name"], d


def test_probes_present():
    found = {name: d for name, d in _deployments()}
    assert WANT <= set(found), WANT - set(found)
    for name in WANT:
        c = found[name]["spec"]["template"]["spec"]["containers"][0]
        assert "readinessProbe" in c and "livenessProbe" in c, name
