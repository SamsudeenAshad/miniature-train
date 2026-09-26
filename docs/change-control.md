# Change-control record (SRS 18.3)

Each entry: ID, proposer, reason, affected requirements, WBS/effort, security/data impact, acceptance impact, decision, date.

| ID | Date | Change | Disposition |
| --- | --- | --- | --- |
| CR-001 | 2026-09-24 | Baseline MT-SRS-WBS-001 v1.0 adopted as build spec | accepted |
| CR-002 | 2026-09-24 | v0.1.0 scope: R1 skeleton + R2 policy slices, R3 excluded | accepted, tagged v0.1.0 |
| CR-003 | 2026-09-24 | Perf/SLO targets recorded as unmeasured; AT-21 deferred to cluster | accepted with limitation noted |
| CR-004 | 2026-09-24 | v0.2.0: governance, risk review, Kubernetes start | accepted, tagged v0.2.0 |
| CR-005 | 2026-09-24 | v0.3.0: deployment depth (rollouts, telemetry, workflows) | accepted, tagged v0.3.0 |
| CR-006 | 2026-09-24 | v0.4.0: hardening (non-root, netpol, secrets) | accepted, tagged v0.4.0 |
| CR-007 | 2026-09-24 | v0.5.0: handover pack (demo, cards, architecture, transfer) | accepted, tagged v0.5.0 |
| CR-008 | 2026-09-24 | v0.6.0: acceptance close-out (DoD, decisions) | accepted, tagged v0.6.0 |
| CR-009 | 2026-09-25 | v0.7.0: HTTP services + console; branch practices adopted | accepted, tagged v0.7.0 |
| CR-010 | 2026-09-25 | v0.8.0: full platform manifests | accepted, tagged v0.8.0 |
| CR-011 | 2026-09-25 | v0.9.0: release engineering (uniform image bumps) | accepted, tagged v0.9.0 |
| CR-012 | 2026-09-25 | v0.10.0: enforced APIs + console wiring | accepted, tagged v0.10.0 |
| CR-013 | 2026-09-25 | v0.11.0: verified wiring (fleet sweeps) | accepted, tagged v0.11.0 |
| CR-014 | 2026-09-26 | v0.12.0: seams + supply chain (audits clean, advisories patched) | accepted, tagged v0.12.0 |
| CR-015 | 2026-09-26 | v0.13.0: persistence path (migrations 001–010) + local dev parity | accepted, tagged v0.13.0 |
| CR-016 | 2026-09-26 | v0.14.0: hardening sweeps + persistence schema | accepted, tagged v0.14.0 |

Baseline is not rewritten to disguise failed experiments; new features require new CR rows.
