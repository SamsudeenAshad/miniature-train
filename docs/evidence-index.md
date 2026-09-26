# Release evidence index (WBS 1.4/11.1)

Maintained per release. Current baseline: v0.22.0 (follow-through).

- Git: `git log --format='%H %an %s'` — all steps by `samsudeenashad`, no co-author trailers.
- Contracts: `packages/contracts/openapi-v1.yaml`, `events/`, `schemas/`.
- Data: `ml/data_generator.py` (`demand-gen-0.1.0`, seed 42, 20160 rows), manifests via `ml/snapshot.py`; entry points `ml/validate_cli.py`, `ml/snapshot_cli.py`; schema chain `infra/migrations/` 001–010.
- Training: `ml/training.py` + `ml/tuning.py` + `ml/cards.py`; gates in `policies/gates.yaml`; runner `workers/training/runner.py`; DAG `infra/workflows/training-dag.yaml`.
- Serving: `services/inference/app/main.py`, `services/control-api/app/main.py`, rollout `infra/k8s/rollout.yaml`, `virtualservice.yaml`, stable/canary services.
- Console: `apps/web/` (React+Vite, `nginx.conf`, `public/config.json`); image + deploy + proxy.
- AIOps: `workers/aiops/` (telemetry, drift, detect, correlate, benchmark, capacity, topology, harness, iforest).
- Recovery: `workers/executor/recovery.py`; policy `policies/quotas.yaml`, `policies/runbooks/`; executor RBAC.
- Governance: `services/control-api/` (authz, audit, security, contracts, notify, incidents, outbox, canary, rollout, release); change-control, risks, acceptance decisions, DoD tracker.
- Infra: `infra/k8s/` (fleet), `infra/telemetry/` (collector, rules, alertmanager, dashboard, monitors), `infra/docker/` (pinned images), `restore.py`, `retention.py`, `health.py`.
- Verification: `python -m pytest -q` (NFR-013) + `npm run check`/`build`; acceptance map `docs/acceptance-index.md`; status `docs/platform-status.md`.
- Releases: notes in `docs/releases/`, tags `v0.1.0` onward; images advance per tag.
