"""Runbook parity tests (Step 134). Code registry matches versioned policy files."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _policies():
    out = {}
    for f in (ROOT / "policies/runbooks").glob("*.yaml"):
        doc = yaml.safe_load(f.read_text())
        out[doc["name"]] = doc
    return out


def test_registry_matches_policy():
    from workers.executor.recovery import RUNBOOKS

    policies = _policies()
    assert set(RUNBOOKS) == set(policies), (set(RUNBOOKS) ^ set(policies))
    for name, spec in RUNBOOKS.items():
        doc = policies[name]
        assert f"v{spec['version']}" == doc["version"], name
        assert spec["risk"] == doc["risk"], name
        assert set(spec["targets"]) == set(doc["allowed_targets"]), name
