"""Release alignment tests (Step 154). Web version tracks the latest platform release."""

import json
import re
import subprocess
import tomllib
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


def test_py_version_matches_release():
    proj = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    major, minor, _ = _latest_release()
    assert proj["version"] == f"{major}.{minor}.0"


def test_every_release_note_has_tag():
    notes = {f.stem for f in (ROOT / "docs/releases").glob("v*.md")}
    tags = set(subprocess.run(["git", "tag", "--list"], capture_output=True, text=True,
                              cwd=ROOT).stdout.split())
    assert notes <= tags, notes - tags
