"""Supply-chain doc tests (Step 159). The policy names every enforced gate."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_supply_chain_gates():
    doc = (ROOT / "docs/supply-chain.md").read_text()
    for gate in ("pip_audit", "npm audit", "test_image_tags"):
        assert gate in doc
