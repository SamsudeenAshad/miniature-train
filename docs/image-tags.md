# Image tag policy

- Every container image is pinned: no `:latest`, no floating tags.
- `miniature-train/*` images advance one release at a time, all together, in a
  single bump commit (uniformity enforced by `test_first_party_tags_uniform`).
- Third-party images pin full upstream versions (e.g. `postgres:16.4`).
- CI does not verify registries; `git log` on `infra/k8s` is the audit trail.
