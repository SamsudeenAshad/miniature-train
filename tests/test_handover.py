"""Handover checks (AT-25, NFR-013 slice)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = ["docs/overview.md", "docs/operator-guide.md", "docs/acceptance-index.md",
                 "docs/evidence-index.md", "docs/adr/ADR-001-modular-monolith.md"]


def test_handover_docs_present():
    missing = [d for d in REQUIRED_DOCS if not (ROOT / d).exists()]
    assert not missing, missing
    index = (ROOT / "docs/evidence-index.md").read_text()
    for path in ("infra/k8s/", "apps/web/", "docs/releases/", "infra/workflows/"):
        assert path in index, path


def test_readme_documents_verification_command():
    readme = (ROOT / "README.md").read_text()
    assert "python -m pytest -q" in readme
    for cmd in ("npm ci", "npm run typecheck", "npm run check", "npm run build", "pip_audit"):
        assert cmd in readme, cmd
