# Web dependency notes

- Vite pinned at 5.4.21 (latest 5.x patch line at time of writing).
- Residual `npm audit` finding: esbuild ≤0.24.2 (moderate, dev-server request
  forgery). It affects `vite dev` only; the shipped artifact is static files
  served by nginx, which never runs the dev server. Fix requires Vite 6
  (breaking); revisit when upgrading the major.
