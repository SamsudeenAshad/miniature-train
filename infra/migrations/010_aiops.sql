-- 010: anomalies + hypotheses (FR-022/025 slice). Scores are not probabilities.
CREATE TABLE anomalies (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  service TEXT NOT NULL,
  window_start BIGINT NOT NULL,
  window_end BIGINT NOT NULL,
  detector_version TEXT NOT NULL,
  score DOUBLE PRECISION NOT NULL,
  threshold DOUBLE PRECISION NOT NULL
);

CREATE TABLE hypotheses (
  incident_id TEXT NOT NULL REFERENCES incidents(id),
  cause TEXT NOT NULL,
  ranker_version TEXT NOT NULL,
  score DOUBLE PRECISION NOT NULL,
  evidence JSONB NOT NULL,
  PRIMARY KEY (incident_id, cause)
);
