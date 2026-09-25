"""Console config tests (Step 111). Mounted config matches web source."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_config_mirror():
    cm = yaml.safe_load((ROOT / "infra/k8s/console-config.yaml").read_text())
    src = json.loads((ROOT / "apps/web/public/config.json").read_text())
    assert json.loads(cm["data"]["config.json"]) == src
    dep = next(d for d in yaml.safe_load_all((ROOT / "infra/k8s/console.yaml").read_text())
               if d.get("kind") == "Deployment")
    spec = dep["spec"]["template"]["spec"]
    assert "runtime-config" in {v["name"] for v in spec["volumes"]}
