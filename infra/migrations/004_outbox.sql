-- 004: outbox events (ADR-02 slice). Committed atomically with state changes.
CREATE TABLE outbox_events (
  event_id TEXT PRIMARY KEY,
  aggregate_id TEXT NOT NULL,
  schema_version TEXT NOT NULL,
  event_type TEXT NOT NULL,
  project_id TEXT NOT NULL,
  payload JSONB NOT NULL,
  delivered BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
