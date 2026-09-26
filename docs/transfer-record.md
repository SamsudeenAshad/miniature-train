# Transfer record (SRS 19.2)

| Area | Owner | Notes |
| --- | --- | --- |
| Cluster/backups/identity/delivery | platform engineer | CronJob `mt-backup`, ExternalSecrets via `platform-store` |
| Benchmarks/features/detector/cards | ml engineer | seeds + frozen digests in eval bundles |
| Incidents/runbook enrollment | service owner | allowlist: rollback + stateless restart only |
| Membership/policy | project admin | independent approver rule; break-glass logged |
| Console/acceptance | frontend/QA | state contract + acceptance index |

Approved environments: local dev, shared eval (pilot). No production adoption without separate readiness review.
Secret handoff: references only (`control-api` and `object-store` ExternalSecrets); values never in repo.
