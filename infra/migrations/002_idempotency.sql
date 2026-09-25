-- 002: idempotency keys (FR-038 slice). One row per key; digest guards payload changes.
CREATE TABLE idempotency_keys (
  key TEXT PRIMARY KEY,
  digest TEXT NOT NULL,
  project_id TEXT REFERENCES projects(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
