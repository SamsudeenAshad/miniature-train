# Acceptance index (AT-01..AT-27 → tests, plus platform sweeps)

## Acceptance scenarios

| AT | Scenario | Tests |
| --- | --- | --- |
| AT-01 | Two-project authz, no self-approval | test_governance, test_api, test_migrations, test_migrate, test_store |
| AT-02 | Invalid datasets quarantined | test_validation |
| AT-03 | Pinned rerun determinism | test_training, test_data_generator, test_snapshot |
| AT-04 | Duplicate/quota/cancel/timeout | test_notify, test_lifecycle, test_schedule, test_contracts_api, test_quota_parity |
| AT-05 | Quality gates block | test_training, test_cards |
| AT-06 | Alias pin, artifact trust | test_training, test_provenance, test_artifacts (in test_tuning) |
| AT-07 | Feature parity, input validation | test_features, test_serving, test_inference_api, test_labels |
| AT-08 | Staging/shadow/promotion/rollback | test_serving, test_rollout |
| AT-09 | Canary stages/pause/abort | test_canary, test_rollout_manifest |
| AT-10 | Abort + reconcile | test_rollout |
| AT-11 | Drift/labels/retraining | test_observability, test_evidently, test_labels |
| AT-12 | Telemetry loss/redaction | test_observability, test_telemetry_manifest, test_collector_deploy, test_loki, test_tempo |
| AT-13 | Anomaly benchmark scoring | test_benchmark, test_aiops, test_harness, test_iforest |
| AT-14 | Correlation + ranking | test_aiops, test_benchmark |
| AT-15 | Incident lifecycle + webhook | test_notify, test_lifecycle, test_outbox |
| AT-16 | Policy/kill-switch denials | test_recovery |
| AT-17 | Fencing/idempotency | test_recovery, test_contracts_api, test_api |
| AT-18 | Console states | test_console, test_demo_script, test_console_config, test_console_proxy, test_console_deploy, test_web_image |
| AT-19 | Audit tamper evidence | test_governance |
| AT-20 | Restore reconcile | test_governance, test_backup, test_backup_job, test_retention |
| AT-21 | Perf profiles | deferred (needs cluster); contract: test_health |
| AT-22 | Degraded operation | test_observability, test_health |
| AT-23 | Retraining cooldown | test_observability |
| AT-24 | Threat-driven | test_governance, test_security, test_secrets_manifest, test_secret_refs, test_hardening, test_executor_rbac, test_inference_rbac, test_token_sweep, test_pod_security, test_supply_chain |
| AT-25 | Handover walkthrough | test_demo, test_handover, test_dod, test_acceptance, test_architecture, test_modelcards, test_transfer, test_runbook, test_platform_status, test_demo_script |
| AT-26 | R3 copilot | out of scope (optional) |
| AT-27 | Capacity bounds | test_capacity, test_resourcequota, test_limitrange, test_resources, test_schedule |

## Platform delivery (manifest contracts, no AT)

test_alerting, test_alertmanager_deploy, test_api_env, test_backup_job, test_collector_deploy,
test_configmap_refs, test_console_config, test_console_deploy, test_console_proxy, test_contracts,
test_dashboard, test_dashboard_provision, test_datasources, test_db, test_dockerfiles,
test_executor_image, test_executor_rbac, test_gitops, test_hardening, test_image_tags,
test_inference_deploy, test_inference_rbac, test_job_hygiene, test_job_lockdown, test_k8s,
test_limitrange, test_loki, test_minio_creds, test_mlflow, test_netpol_egress, test_networkpolicy,
test_object_store, test_openapi_parity, test_outbox, test_pdb, test_platform_reqs,
test_platform_status, test_pod_security, test_prediction_services, test_probes,
test_prometheus_config, test_repo_layout, test_resourcequota, test_resources, test_rollout_manifest,
test_runbook, test_runbook_parity, test_runner, test_schedule, test_secret_refs, test_secrets_manifest, test_security,
test_selectors, test_servicemonitors, test_snapshot, test_sync_waves, test_telemetry_deploy,
test_telemetry_manifest, test_tempo, test_token_sweep, test_training_image, test_training_sa,
test_tuning, test_virtualservice, test_volumes, test_web_image, test_workflow,
test_cards, test_evidently, test_harness, test_iforest, test_provenance, test_api, test_contracts_api,
test_inference_api, test_labels, test_console, test_transfer, test_modelcards, test_dod,
test_acceptance, test_architecture, test_handover, test_acceptance_coverage, test_release_align
