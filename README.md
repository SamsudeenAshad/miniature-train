# miniature-train

An integrated MLOps and AIOps platform for reproducible machine learning, observable services, and controlled incident recovery.

Spec: `docs/overview.md` (baseline MT-SRS-WBS-001 v1.0, R1/R2 scope; R3 optional).
Name is the software project name; railway/train control is out of scope.

## Repository layout (SRS 13.5)

- `apps/web/` — console application and UI checks
- `services/control-api/` — authorization, project, lifecycle, incident, action APIs
- `services/inference/` — prediction contract and packaged model loading
- `workers/training/` — trusted template runner and Argo adapter
- `workers/aiops/` — feature aggregation, detection, grouping, ranking
- `workers/executor/` — fenced runbook execution and verification
- `packages/contracts/` — OpenAPI, JSON schemas, events, shared identifiers
- `ml/` — DVC definitions, feature logic, model templates, evaluation scripts
- `infra/` — Compose, Helm, GitOps, telemetry, network, secret-reference config
- `policies/` — versioned gates, quotas, environment policies, runbooks
- `tests/` — contract, integration, security, workload, fault scenarios
- `docs/` — SRS/WBS, architecture decisions, model cards, reports, runbooks, handover

## Quickstart

Requires Python 3.13 (CPU-only, no GPU) and Node 22 for the console.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
python -m pip_audit -r requirements.txt
python -m ml.data_generator --seed 42 --out data/demand.csv --manifest data/manifest.json
```

```powershell
cd apps/web
npm ci
npm run typecheck
npm run check
npm run build
```

Verification (NFR-013): `python -m pytest -q` plus the four web commands above
must pass on a fresh checkout.

## Local stack (needs Docker)

```powershell
$env:POSTGRES_PASSWORD = "dev-only-secret"
docker compose -f infra/docker-compose.yml up --build
# console http://localhost:8080, control API http://localhost:8000
```

## Status

Shipped through v0.19.0: reproducible data → training → registry → HTTP services
→ canary delivery → AIOps → governed recovery, with manifests, console, and
fleet-wide contract tests. See `docs/releases/` for per-release notes and
`docs/platform-status.md` for what is proven vs pending a cluster.
