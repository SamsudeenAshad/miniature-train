"""Runbook tests (Step 123). The runbook names every enforcing sweep."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runbook_lists_sweeps():
    doc = (ROOT / "docs/runbook-add-service.md").read_text()
    for sweep in ("test_probes", "test_secret_refs", "test_configmap_refs", "test_selectors",
                  "sync-wave", "uniform", "WANT"):
        assert sweep in doc
