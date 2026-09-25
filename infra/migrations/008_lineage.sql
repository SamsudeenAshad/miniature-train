-- 008: ML lineage (OBJ-01 slice). Digests chain snapshot → run → model version.
CREATE TABLE dataset_snapshots (
  digest TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  source TEXT NOT NULL,
  schema_version TEXT NOT NULL,
  row_count INTEGER NOT NULL,
  validation_status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE pipeline_runs (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  snapshot_digest TEXT NOT NULL REFERENCES dataset_snapshots(digest),
  feature_version TEXT NOT NULL,
  code_commit TEXT NOT NULL,
  seed INTEGER NOT NULL,
  state TEXT NOT NULL DEFAULT 'queued',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE model_versions (
  version SERIAL PRIMARY KEY,
  project_id TEXT NOT NULL,
  run_id TEXT NOT NULL REFERENCES pipeline_runs(id),
  artifact_digest TEXT NOT NULL UNIQUE,
  model_card_digest TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
