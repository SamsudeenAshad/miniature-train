# Restore runbook (FR-036, RTO 2h / RPO 24h targets)

1. Halt writers; snapshot current state.
2. Restore metadata + objects from daily point (age ≤24h).
3. Verify digests (`infra/restore.py`), policy versions, registry pointers, release refs.
4. Reapply deletion tombstones (`infra/retention.py`).
5. Reconcile Git vs observed; read-only until `verified`.
6. Record elapsed time vs 2h RTO target.
