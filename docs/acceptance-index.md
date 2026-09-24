# Acceptance index (AT-01..AT-27 → tests)

| AT | Scenario | Test |
| --- | --- | --- |
| AT-01 | Two-project authz, no self-approval | test_governance |
| AT-02 | Invalid datasets quarantined | test_validation |
| AT-03 | Pinned rerun determinism | test_training, test_data_generator |
| AT-04 | Duplicate/quota/cancel/timeout | test_notify (quota) |
| AT-05 | Quality gates block | test_training |
| AT-06 | Alias pin, artifact trust | test_training |
| AT-07 | Feature parity, input validation | test_features, test_serving |
| AT-08 | Staging/shadow/promotion/rollback | test_serving |
| AT-09 | Canary stages/pause/abort | test_canary |
| AT-10 | Abort + reconcile | test_rollout |
| AT-11 | Drift/labels/retraining | test_observability |
| AT-12 | Telemetry loss/redaction | test_observability |
| AT-13 | Anomaly benchmark scoring | test_benchmark, test_aiops |
| AT-14 | Correlation + ranking | test_aiops, test_benchmark |
| AT-15 | Incident lifecycle + webhook | test_notify |
| AT-16 | Policy/kill-switch denials | test_recovery |
| AT-17 | Fencing/idempotency | test_recovery |
| AT-18 | Console states | test_console |
| AT-19 | Audit tamper evidence | test_governance |
| AT-20 | Restore reconcile | test_governance |
| AT-21 | Perf profiles | deferred (needs cluster) |
| AT-22 | Degraded operation | test_observability |
| AT-23 | Retraining cooldown | test_observability |
| AT-24 | Threat-driven | test_governance |
| AT-25 | Handover walkthrough | test_demo |
| AT-26 | R3 copilot | out of scope (optional) |
| AT-27 | Capacity bounds | test_capacity |
