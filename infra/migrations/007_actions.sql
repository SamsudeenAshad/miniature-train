-- 007: action lifecycle (FR-027/028/029 slice). Plan hash binds approval to execution.
CREATE TABLE action_requests (
  id TEXT PRIMARY KEY,
  incident_id TEXT REFERENCES incidents(id),
  runbook_name TEXT NOT NULL,
  runbook_version INTEGER NOT NULL,
  target TEXT NOT NULL,
  target_digest TEXT NOT NULL,
  plan_hash TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'proposed',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE approvals (
  id BIGSERIAL PRIMARY KEY,
  action_id TEXT NOT NULL REFERENCES action_requests(id),
  approver TEXT NOT NULL,
  plan_hash TEXT NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  decision TEXT NOT NULL,
  reason TEXT NOT NULL
);

CREATE TABLE executions (
  id BIGSERIAL PRIMARY KEY,
  action_id TEXT NOT NULL REFERENCES action_requests(id),
  executor TEXT NOT NULL,
  fencing_token TEXT NOT NULL,
  result TEXT NOT NULL,
  verified BOOLEAN NOT NULL DEFAULT FALSE
);
