"""Acceptance coverage tests (Step 129). Every test file is indexed."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_every_test_file_indexed():
    index = (ROOT / "docs/acceptance-index.md").read_text()
    missing = []
    for f in sorted((ROOT / "tests").glob("test_*.py")):
        if f.stem not in index:
            missing.append(f.stem)
    assert not missing, missing
    assert re.search(r"\| AT-01 \|.*\| AT-27 \|", index, re.S)
