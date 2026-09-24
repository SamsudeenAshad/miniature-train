"""Console deploy tests (Step 102). Hardened static frontend."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_console_serves():
    docs = list(yaml.safe_load_all((ROOT / "console.yaml").read_text()))
    dep = next(d for d in docs if d["kind"] == "Deployment")
    c = dep["spec"]["template"]["spec"]["containers"][0]
    assert c["image"].startswith("miniature-train/console:")
    assert "readinessProbe" in c and "livenessProbe" in c
