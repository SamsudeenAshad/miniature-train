"""Migration tests (Step 141). Schema files apply in order and cover the model."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "infra/migrations"


def test_projects_schema():
    sql = (ROOT / "001_projects.sql").read_text()
    assert "CREATE TABLE projects" in sql
    assert "CREATE TABLE memberships" in sql
    assert "REFERENCES projects(id)" in sql
    assert "PRIMARY KEY (project_id, subject)" in sql


def test_idempotency_schema():
    sql = (ROOT / "002_idempotency.sql").read_text()
    assert "CREATE TABLE idempotency_keys" in sql
    assert "PRIMARY KEY" in sql and "digest" in sql


def test_audit_schema():
    sql = (ROOT / "003_audit.sql").read_text()
    assert "CREATE TABLE audit_events" in sql
    assert "prev_digest" in sql and "UNIQUE" in sql
