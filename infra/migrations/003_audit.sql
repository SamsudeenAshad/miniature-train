-- 003: audit events (FR-035 slice). Append-only; no UPDATE/DELETE grants to app role.
CREATE TABLE audit_events (
  id BIGSERIAL PRIMARY KEY,
  actor TEXT NOT NULL,
  project_id TEXT NOT NULL,
  action TEXT NOT NULL,
  object TEXT NOT NULL,
  outcome TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  correlation_id TEXT NOT NULL,
  prev_digest TEXT NOT NULL,
  digest TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
