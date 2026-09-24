"""PDB tests (Step 84). Budget covers the two-replica inference fleet."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "infra/k8s"


def test_pdb_matches_inference():
    docs = list(yaml.safe_load_all((ROOT / "pdb.yaml").read_text()))
    by_name = {d["metadata"]["name"]: d for d in docs}
    assert by_name["inference"]["spec"]["minAvailable"] == 1
    assert by_name["control-api"]["spec"]["maxUnavailable"] == 0
    dep = next(d for d in yaml.safe_load_all((ROOT / "inference.yaml").read_text()) if d["kind"] == "Deployment")
    assert dep["spec"]["replicas"] == 2
    assert dep["spec"]["template"]["metadata"]["labels"]["app"] == "inference"
