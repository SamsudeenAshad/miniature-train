# Controller ownership (SRS 11.6)

- Git + release controller own image/model digests and deployment config.
- Argo Rollouts owns rollout progression and traffic-weight fields; Argo CD ignores them (see `ignoreDifferences`).
- Abort restores stable traffic; release controller records failed revision + desired-state correction.
- Until Git == observed, state is `reconciliation_required`.
- No autonomous scaler baseline; if HPA added later, it owns replicas and runbooks change bounds instead.
- Model rollback never reverses DB migrations: expand/contract or explicit recovery required first.
