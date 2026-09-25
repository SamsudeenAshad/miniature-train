"""Store seam tests (Step 152). Routes share one replaceable backend."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_seam_single_backend():
    store = _load("store", "services/control-api/app/store.py")
    api = _load("api_main", "services/control-api/app/main.py")
    assert api._store.backend == "memory"
    assert api._projects is api._store.projects
    assert api._members is api._store.members
