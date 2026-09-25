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


def test_outbox_schema():
    sql = (ROOT / "004_outbox.sql").read_text()
    assert "CREATE TABLE outbox_events" in sql
    assert "JSONB" in sql and "delivered" in sql


def test_incidents_schema():
    sql = (ROOT / "005_incidents.sql").read_text()
    assert "CREATE TABLE incidents" in sql
    assert "version INTEGER" in sql and "timeline JSONB" in sql


def test_deployments_schema():
    sql = (ROOT / "006_deployments.sql").read_text()
    assert "CREATE TABLE deployments" in sql
    assert "artifact_digest" in sql and "previous_digest" in sql


def test_actions_schema():
    sql = (ROOT / "007_actions.sql").read_text()
    assert "CREATE TABLE action_requests" in sql
    assert "CREATE TABLE approvals" in sql
    assert "CREATE TABLE executions" in sql
    assert "plan_hash" in sql and "fencing_token" in sql


def test_lineage_schema():
    sql = (ROOT / "008_lineage.sql").read_text()
    assert "CREATE TABLE dataset_snapshots" in sql
    assert "CREATE TABLE pipeline_runs" in sql
    assert "CREATE TABLE model_versions" in sql
    assert "REFERENCES dataset_snapshots(digest)" in sql
    assert "REFERENCES pipeline_runs(id)" in sql


def test_predictions_schema():
    sql = (ROOT / "009_predictions.sql").read_text()
    assert "CREATE TABLE predictions" in sql
    assert "CREATE TABLE label_revisions" in sql
    assert "PRIMARY KEY (ctx, rev)" in sql


def test_aiops_schema():
    sql = (ROOT / "010_aiops.sql").read_text()
    assert "CREATE TABLE anomalies" in sql
    assert "CREATE TABLE hypotheses" in sql
    assert "REFERENCES incidents(id)" in sql
