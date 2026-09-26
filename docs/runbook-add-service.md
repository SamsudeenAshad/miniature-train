# Runbook: add a service

1. Deployment + Service in `infra/k8s/` (pinned image, probes, requests+limits,
   non-root, tokenless, seccomp, dedicated SA where needed).
2. Probes must exist — `test_probes.py` WANT list gains the app name.
3. Service ports referenced by monitors/dashboards must be named.
4. Secrets only by reference (`test_secret_refs.py`); ConfigMaps must exist
   (`test_configmap_refs.py`); selectors must resolve (`test_selectors.py`).
5. NetworkPolicy egress: add the Service port or the sweep fails.
6. Stateful data syncs on wave `0` via `sync-wave` annotation; apps default to wave `1`.
7. Disruption budgets: replicas get `minAvailable`, singletons get `maxUnavailable: 0`.
8. New tables ship as sequenced migrations in `infra/migrations/` (gapless numbering tested).
9. Metrics need a ServiceMonitor with the NFR-003 30s interval to be scraped.
10. Image built from `infra/docker/`; first-party tags advance uniformly.
11. Local compose entry with healthcheck and healthy-only dependencies.
12. New routes join the OpenAPI contract with parity tests (`test_openapi_parity.py`).
13. Docs: `platform-status.md` (if pilot-grade), `evidence-index.md` baseline row.

Run `python -m pytest -q` — the fleet sweeps catch every missed touchpoint.
