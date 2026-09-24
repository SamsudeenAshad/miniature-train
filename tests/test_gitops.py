"""GitOps tests (Step 34, SRS 11.6 slice)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_app_ignores_rollout_fields():
    app = yaml.safe_load((ROOT / "infra/gitops/app.yaml").read_text())
    assert app["spec"]["source"]["path"] == "infra/k8s"
    ignored = app["spec"]["ignoreDifferences"][0]
    assert ignored["kind"] == "Rollout"
    doc = (ROOT / "docs/controller-ownership.md").read_text()
    assert "reconciliation_required" in doc
