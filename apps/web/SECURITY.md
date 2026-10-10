# Web dependency notes

- Vite pinned at 5.4.21 (latest 5.x patch line at time of writing).
- Residual `npm audit` findings, both dev-server scope only (the shipped artifact
  is static files served by nginx, which never runs the dev server):
  - esbuild ≤0.24.2 (moderate, dev-server request forgery).
  - vite ≤6.4.2 advisory set (high, dev-server `fs.deny` bypasses).
  Fix requires Vite 6 (breaking); revisit when upgrading the major.
- Patched without breakage: `source-map-js` high (DoS) via `npm audit fix` (Step 320).
