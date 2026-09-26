# Supply-chain notes (NFR-008 slice)

- Python: `python -m pip_audit -r requirements.txt` runs in CI and must be clean.
  Pin upgrades are their own commits with the full suite green.
- Web: `npm audit` reviewed per dependency change. Dev-server-only findings do not
  ship (production is static nginx); details live in `apps/web/SECURITY.md`.
- Images: every tag pinned, swept by `test_image_tags.py`; first-party tags advance
  uniformly with releases.
- Residuals are documented with scope and revisit condition — never silently accepted.
