"""Object-store credential tests (Step 75). No plaintext; job creates MLflow bucket."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def _docs(name: str):
    return list(yaml.safe_load_all((ROOT / name).read_text()))


def test_minio_creds_by_reference():
    es = next(d for d in _docs("object-store-secret.yaml") if d["kind"] == "ExternalSecret")
    assert es["spec"]["target"]["name"] == "object-store"
    sts = next(d for d in _docs("object-store.yaml") if d["kind"] == "StatefulSet")
    env = {e["name"]: e for e in sts["spec"]["template"]["spec"]["containers"][0]["env"]}
    assert env["MINIO_ROOT_USER"]["valueFrom"]["secretKeyRef"]["name"] == "object-store"
    job = next(d for d in _docs("bucket-job.yaml") if d["kind"] == "Job")
    args = " ".join(job["spec"]["template"]["spec"]["containers"][0]["args"])
    assert "store/miniature-train/mlflow" in args
    blob = (ROOT / "object-store.yaml").read_text() + (ROOT / "bucket-job.yaml").read_text()
    assert "password: " not in blob.lower().replace("root-password", "").replace("secretkeyref", "")
