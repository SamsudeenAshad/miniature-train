"""Migration ordering tests (Step 142)."""

from pathlib import Path

from infra.migrate import pending

ROOT = Path(__file__).resolve().parents[1] / "infra/migrations"


def test_pending_in_filename_order(tmp_path):
    (tmp_path / "002_b.sql").write_text("x")
    (tmp_path / "001_a.sql").write_text("x")
    assert [p.name for p in pending(tmp_path, set())] == ["001_a.sql", "002_b.sql"]
    assert [p.name for p in pending(tmp_path, {"001_a.sql"})] == ["002_b.sql"]


def test_real_dir_has_sequenced_start():
    assert pending(ROOT, set())[0].name == "001_projects.sql"


def test_numbering_gapless():
    names = [p.name for p in pending(ROOT, set())]
    numbers = [int(n.split("_")[0]) for n in names]
    assert numbers == list(range(1, len(numbers) + 1))
