# Pilot acceptance decisions (SRS 14.4)

| Release | Decision | Date | Note |
| --- | --- | --- | --- |
| R1 skeleton | pilot-accepted with limitations | 2026-09-24 | dataset-to-service path works; perf unmeasured |
| R2 policy slices | pilot-accepted with limitations | 2026-09-24 | guards/rollback/recovery enforced in code; cluster proof pending |
| v0.7.0–v0.12.0 platform + APIs | pilot-accepted with limitations | 2026-09-26 | manifests statically verified; fleet sweeps green; cluster apply pending |
| v0.13.0 persistence + local dev | pilot-accepted with limitations | 2026-09-26 | schema chain tested; driver pending; compose parity checked |
| v0.14.0 hardening + schema | pilot-accepted with limitations | 2026-09-26 | sweeps fleet-wide incl. workflows; audits clean; cluster pending |
| v0.15.0 governance + local dev | pilot-accepted with limitations | 2026-09-26 | compose ordered + healthy; docs current; cluster pending |
| 30-day 99.5% SLO | pending | — | assessed only after 30 days of valid probes |
| R3 copilot | not selected | 2026-09-24 | tracked separately; core unaffected |
