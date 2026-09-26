# Contributing — branch practices

## Branches

- `main` is the releasable branch. Never commit directly except release notes.
- Day-to-day work lands on `dev/round2` as one commit per step, merged to `main`
  with `git merge --no-ff` after green verification.
- New `feat/*` or `fix/*` branches only for parallel or risky work that must stay
  isolated; delete them (local and remote) right after merging.
- After any direct-to-main commit (releases), merge `main` back into `dev/round2`
  before the next step so the branches can't drift.
- Keep the branch list short: `main`, `dev/rolling`, and at most one active topic.

## Merging to main

1. `python -m pytest -q` green (and `npm run check` + `npm run build` if `apps/web` touched).
2. Verify first, merge second: never chain `pytest; ... merge` in one command —
   the merge runs even when tests fail. Read the result, then merge.
3. Commit as `samsudeenashad`, no `Co-authored-by` trailers.
4. Push branch, merge with `git merge --no-ff -m "Merge ..."` on `main`.
5. Push `main`.

## Releases

- Release notes in `docs/releases/vX.Y.Z.md` plus version bumps, committed to `main`.
- Tag `vX.Y.Z` on the release commit, then verify, then push both: the
  notes↔tags parity test fails until the tag exists.
- Annotated tag pushed; GitHub Release object drafted from the tag in the web UI.
- Patch/minor/major: minor per step-batch, major on breaking API/contract change.

## CI

`ci.yml` runs pytest, pip-audit, and the web checks/build. It clones with full
history (`fetch-depth: 0`) because the release↔tag parity tests need tags —
a shallow clone fails them with zero tags present.
