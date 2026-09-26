# Contributing — branch practices

## Branches

- `main` is the releasable branch. Never commit directly except release notes.
- Feature work: `feat/<scope>` branched from `main`.
- Fixes: `fix/<scope>` branched from `main`.
- One step = one branch = one merge.

## Merging to main

1. `python -m pytest -q` green (and `npm run check` + `npm run build` if `apps/web` touched).
2. Verify first, merge second: never chain `pytest; ... merge` in one command —
   the merge runs even when tests fail. Read the result, then merge.
3. Commit as `samsudeenashad`, no `Co-authored-by` trailers.
3. Push branch, merge with `git merge --no-ff feat/<scope> -m "Merge ..."` on `main`.
4. Push `main`.

## Releases

- Release notes in `docs/releases/vX.Y.Z.md`, committed to `main`.
- Annotated tag `vX.Y.Z` pushed; GitHub Release object drafted from the tag in the web UI.
- Patch/minor/major: minor per step-batch, major on breaking API/contract change.
