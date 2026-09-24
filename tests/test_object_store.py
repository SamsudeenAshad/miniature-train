"""Object store tests (Step 60)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_object_store_s3():
    docs = list(yaml.safe_load_all((ROOT / "object-store.yaml").read_text()))
    sts = next(d for d in docs if d["kind"] == "StatefulSet")
    img = sts["spec"]["template"]["spec"]["containers"][0]["image"]
    assert img.startswith("minio/minio:")
    svc = next(d for d in docs if d["kind"] == "Service")
    assert any(p["port"] == 9000 for p in svc["spec"]["ports"])
