# Operator guide (WBS 11.1)

## Local stack

```powershell
$env:POSTGRES_PASSWORD = "dev-only-secret"
docker compose -f infra/docker-compose.yml up --build
```

Console `http://localhost:8080`, control API `http://localhost:8000`.

## Projects API

- Identity is pilot headers: `X-Subject` (who) and `X-Role` (must be
  `project_admin` to create). Reads use stored membership; strangers get 404.
- Creation accepts `Idempotency-Key`: same key + payload replays the same
  project (`200` + `Location`); same key + different payload is `409`.
- Callers without headers are denied (403 create, 404 read) — there is no anonymous access.
- Every create/replay answers a `Location: /v1/projects/{id}` header.

## ML lifecycle

1. Seed demo: `python -m ml.data_generator --seed 42 --out data/demand.csv --manifest data/manifest.json`
2. Validate: quarantine report must be `accepted` before training.
3. Train/evaluate: check gates; blocked releases stay `proposed`; cards in `ml/cards.py`.
4. Predict: payloads over 10 KB are rejected with 422 before any model work.
5. Migrations apply in filename order (`infra/migrate.py`); numbering must stay gapless.

## Incidents and recovery

1. Monitor: telemetry health `degraded` inhibits actions; drift needs 500 obs.
2. Incident: correlate alerts, rank hypotheses (correlation, not causation).
3. Recover: dry-run → approve exact plan hash → fenced execute → verify.
4. Kill switch stops new mutations; in-flight verification continues.
5. Approval TTL 15 min, evidence TTL 2 min, cooldown 15 min (`policies/action-policy.yaml`).
