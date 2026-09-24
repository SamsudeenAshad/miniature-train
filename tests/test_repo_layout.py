"""Repo layout must match SRS 13.5 (WBS 2.1)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "apps/web",
    "services/control-api",
    "services/inference",
    "workers/training",
    "workers/aiops",
    "workers/executor",
    "packages/contracts",
    "ml",
    "infra",
    "policies",
    "tests",
    "docs",
]


def test_required_layout():
    missing = [p for p in REQUIRED if not (ROOT / p).is_dir()]
    assert not missing, f"missing layout dirs: {missing}"
