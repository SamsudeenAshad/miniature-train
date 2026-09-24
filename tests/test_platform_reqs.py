"""Platform requirement tests (Step 71). Foreign CRD kinds map to controllers."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_controllers_documented():
    doc = (ROOT / "docs/platform-requirements.md").read_text()
    for kind in ("Rollout", "WorkflowTemplate", "Application", "VirtualService", "ServiceMonitor", "ExternalSecret"):
        assert kind in doc
