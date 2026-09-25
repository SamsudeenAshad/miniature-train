-- 006: deployments (FR-011/013 slice). Inputs immutable; state versioned for locking.
CREATE TABLE deployments (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  environment TEXT NOT NULL,
  model_version INTEGER NOT NULL,
  artifact_digest TEXT NOT NULL,
  image_digest TEXT NOT NULL,
  git_revision TEXT NOT NULL,
  rollout_state TEXT NOT NULL DEFAULT 'proposed',
  previous_digest TEXT,
  state_version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
