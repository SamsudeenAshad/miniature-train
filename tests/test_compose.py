"""Compose tests (Step 166). Local-dev file is consistent and secret-free."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_compose_consistent():
    doc = yaml.safe_load((ROOT / "infra/docker-compose.yml").read_text())
    api = doc["services"]["control-api"]["build"]
    assert api["context"] == ".."
    assert (ROOT / api["dockerfile"]).exists()
    blob = (ROOT / "infra/docker-compose.yml").read_text()
    assert "POSTGRES_PASSWORD=mt" not in blob
    assert doc["services"]["db"]["image"] == "postgres:16.4"
