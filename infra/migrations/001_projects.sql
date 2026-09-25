-- 001: projects + memberships (SRS 9.1 slice). Applied in order by filename.
CREATE TABLE projects (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  owner TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE memberships (
  project_id TEXT NOT NULL REFERENCES projects(id),
  subject TEXT NOT NULL,
  role TEXT NOT NULL,
  PRIMARY KEY (project_id, subject)
);
