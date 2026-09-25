-- 005: incidents (FR-026 slice). Optimistic locking via version; timeline as JSONB.
CREATE TABLE incidents (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  environment TEXT NOT NULL,
  severity TEXT NOT NULL,
  state TEXT NOT NULL DEFAULT 'open',
  owner TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  timeline JSONB NOT NULL DEFAULT '["opened"]',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
