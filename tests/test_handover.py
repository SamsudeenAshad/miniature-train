"""Handover checks (AT-25, NFR-013 slice)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = ["docs/overview.md", "docs/operator-guide.md", "docs/acceptance-index.md",
                 "docs/evidence-index.md", "docs/adr/ADR-001-modular-monolith.md",
                 "docs/demo-script.md", "docs/architecture.md", "docs/transfer-record.md",
                 "docs/runbook-add-service.md", "docs/supply-chain.md", "docs/platform-status.md",
                 "docs/change-control.md", "docs/risks.md", "docs/acceptance-decisions.md",
                 "docs/definition-of-done.md", "docs/controller-ownership.md",
                 "docs/restore-runbook.md", "docs/image-tags.md", "docs/platform-requirements.md",
                 "CONTRIBUTING.md"]


def test_handover_docs_present():
    missing = [d for d in REQUIRED_DOCS if not (ROOT / d).exists()]
    assert not missing, missing
    cards = list((ROOT / "docs/model-cards").glob("*.md"))
    assert len(cards) >= 2, cards
    assert list((ROOT / "docs/releases").glob("v*.md")), "no release notes"
    assert list((ROOT / "infra/migrations").glob("*.sql")), "no migrations"
    guide = (ROOT / "docs/operator-guide.md").read_text()
    for keyword in ("Idempotency-Key", "Location", "X-Subject", "action-policy"):
        assert keyword in guide, keyword
    index = (ROOT / "docs/evidence-index.md").read_text()
    for path in ("infra/k8s/", "apps/web/", "docs/releases/", "infra/workflows/"):
        assert path in index, path


def test_readme_documents_verification_command():
    readme = (ROOT / "README.md").read_text()
    assert "python -m pytest -q" in readme
    for cmd in ("npm ci", "npm run typecheck", "npm run check", "npm run build", "pip_audit"):
        assert cmd in readme, cmd
    assert "docker compose" in readme and "POSTGRES_PASSWORD" in readme
