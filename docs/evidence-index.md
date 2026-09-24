# Release evidence index (WBS 1.4/11.1)

Maintained per release. Current baseline: R1 skeleton + R2 policy slices.

- Git: `git log --format='%H %an %s'` — all steps by `samsudeenashad`, no co-author trailers.
- Contracts: `packages/contracts/openapi-v1.yaml`, `events/`, `schemas/`.
- Data: `ml/data_generator.py` (`demand-gen-0.1.0`, seed 42, 20160 rows), manifests via `ml/snapshot.py`.
- Training: `ml/training.py` + `ml/tuning.py` + `ml/cards.py`; gates in `policies/gates.yaml`.
- Serving: `services/inference/predict.py`, `services/control-api/release.py`, `canary.py`, `rollout.py`.
- AIOps: `workers/aiops/` (telemetry, drift, detect, correlate, benchmark, capacity, topology).
- Recovery: `workers/executor/recovery.py`; policy `policies/quotas.yaml`, `policies/runbooks/`.
- Governance: `services/control-api/authz.py`, `audit.py`, `security.py`, `contracts.py`, `notify.py`, `incidents.py`.
- Infra: `infra/docker-compose.yml`, `restore.py`, `retention.py`.
- Verification: `python -m pytest -q` (NFR-013); acceptance map `docs/acceptance-index.md`.
