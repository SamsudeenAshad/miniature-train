"""Console state contract test (FR-033 slice, NFR-012)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_state_contract():
    c = json.loads((ROOT / "apps/web/state-contract.json").read_text())
    assert set(c["required_context"]) == {"project", "environment"}
    for s in ("overview", "incident", "action", "audit"):
        assert s in c["screens"]
    for st in ("loading", "empty", "denied", "disconnected", "partial", "stale"):
        assert st in c["states"]
    assert c["rules"]["approval_separate_from_execution"] is True
    assert c["rules"]["show_risk_target_before_approve"] is True


def test_acceptance_index_covers_committed_scope():
    idx = (ROOT / "docs/acceptance-index.md").read_text()
    for at in ("AT-01", "AT-08", "AT-13", "AT-16", "AT-25"):
        assert at in idx
