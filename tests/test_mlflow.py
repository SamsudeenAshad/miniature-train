"""MLflow deploy tests (Step 70). Pilot store only: sqlite + emptyDir, S3 artifacts."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_mlflow_pinned_and_served():
    docs = list(yaml.safe_load_all((ROOT / "mlflow.yaml").read_text()))
    dep = next(d for d in docs if d["kind"] == "Deployment")
    c = dep["spec"]["template"]["spec"]["containers"][0]
    assert c["image"] == "ghcr.io/mlflow/mlflow:v2.16.0"
    assert any("s3://miniature-train/mlflow" in a for a in c["args"])
    svc = next(d for d in docs if d["kind"] == "Service")
    assert svc["spec"]["selector"] == {"app": "mlflow"}
