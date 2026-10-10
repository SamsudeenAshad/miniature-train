"""Supply-chain doc tests (Step 159). The policy names every enforced gate."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_supply_chain_gates():
    doc = (ROOT / "docs/supply-chain.md").read_text()
    for gate in ("pip_audit", "npm audit", "test_image_tags"):
        assert gate in doc
    web_notes = (ROOT / "apps/web/SECURITY.md").read_text()
    for residual in ("esbuild", "vite", "source-map-js"):
        assert residual in web_notes, residual


def test_requirements_pinned():
    lines = (ROOT / "requirements.txt").read_text().splitlines()
    entries = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    assert entries, "requirements.txt has no entries"
    for entry in entries:
        assert "==" in entry, entry


def test_web_vite_pin_matches_notes():
    import json
    import re

    pkg = json.loads((ROOT / "apps/web/package.json").read_text())
    vite = pkg["devDependencies"]["vite"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", vite), vite
    notes = (ROOT / "apps/web/SECURITY.md").read_text()
    assert f"Vite pinned at {vite}" in notes, vite
    lock = json.loads((ROOT / "apps/web/package-lock.json").read_text())
    assert lock["packages"]["node_modules/vite"]["version"] == vite
