"""Release alignment tests (Step 154). Web version tracks the latest platform release."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _latest_release():
    versions = []
    for f in (ROOT / "docs/releases").glob("v*.md"):
        m = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)\.md", f.name)
        if m:
            versions.append(tuple(int(x) for x in m.groups()))
    return max(versions)


def test_web_version_matches_release():
    pkg = json.loads((ROOT / "apps/web/package.json").read_text())
    major, minor, _ = _latest_release()
    assert pkg["version"] == f"{major}.{minor}.0"
