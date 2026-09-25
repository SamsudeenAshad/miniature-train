-- 009: predictions + labels (FR-017 slice). Context-keyed; labels versioned by revision.
CREATE TABLE predictions (
  ctx TEXT NOT NULL,
  project_id TEXT NOT NULL,
  model_version INTEGER NOT NULL,
  event_time BIGINT NOT NULL,
  pred DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (ctx, model_version)
);

CREATE TABLE label_revisions (
  ctx TEXT NOT NULL,
  project_id TEXT NOT NULL,
  label_time BIGINT NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  rev INTEGER NOT NULL,
  PRIMARY KEY (ctx, rev)
);
