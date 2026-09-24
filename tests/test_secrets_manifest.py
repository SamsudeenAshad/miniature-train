"""Secret reference tests (Step 43, NFR-008 slice)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_no_plaintext_secrets():
    es = yaml.safe_load((ROOT / "externalsecret.yaml").read_text())
    assert es["spec"]["refreshInterval"] == "1h"
    keys = {d["secretKey"] for d in es["spec"]["data"]}
    assert {"database-password", "registry-token"} <= keys
    assert "password" not in str(es["spec"]["data"]).lower().replace("database-password", "").replace("secretkey", "")
