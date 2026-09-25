"""Console proxy tests (Step 105). Nginx routes match config.json and service names."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
K8S = ROOT / "infra/k8s"


def _services():
    names = set()
    for f in K8S.glob("*.yaml"):
        for d in yaml.safe_load_all(f.read_text()):
            if d and d.get("kind") == "Service":
                names.add(d["metadata"]["name"])
    return names


def test_proxy_matches_backends():
    nginx = (ROOT / "apps/web/nginx.conf").read_text()
    cfg = json.loads((ROOT / "apps/web/public/config.json").read_text())
    assert "/api/control/" in nginx and "/api/inference/" in nginx
    assert cfg["controlApiUrl"].startswith("/api/control")
    assert cfg["inferenceUrl"].startswith("/api/inference")
    svcs = _services()
    assert "control-api" in svcs and "inference" in svcs
    assert "proxy_pass http://control-api:80/" in nginx
    assert "proxy_pass http://inference:80/" in nginx
    df = (ROOT / "infra/docker/web.Dockerfile").read_text()
    assert "nginx.conf /etc/nginx/conf.d/default.conf" in df
