# Image tag policy

- Every container image is pinned: no `:latest`, no floating tags.
- `miniature-train/*` images advance one release at a time; the bump is its own
  commit so rollbacks stay exact.
- Third-party images pin full upstream versions (e.g. `postgres:16.4`).
- CI does not verify registries; `git log` on `infra/k8s` is the audit trail.
