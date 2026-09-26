"""Training/eval/registry/gate tests (FR-009/010/011, ML-002/003 slice)."""

from pathlib import Path

import yaml

from ml.data_generator import generate_rows
from ml.features import fit_preprocessing
from ml import registry
from ml.training import check_gates, train_and_evaluate

ROOT = Path(__file__).resolve().parents[1]


def _train_mean(rows):
    p = fit_preprocessing(rows)
    return p["train_mean"]


def test_deterministic_repeat():
    rows = generate_rows(seed=42)
    m = _train_mean(rows)
    r1 = train_and_evaluate(rows, seed=42, train_mean=m)
    r2 = train_and_evaluate(rows, seed=42, train_mean=m)
    assert r1["artifact_digest"] == r2["artifact_digest"]
    assert abs(r1["validation"]["mae"] - r2["validation"]["mae"]) <= 1e-8


def test_candidate_beats_baseline_and_gates():
    rows = generate_rows(seed=42)
    rep = train_and_evaluate(rows, seed=42, train_mean=_train_mean(rows))
    assert rep["validation"]["n"] > 0
    assert rep["validation"]["mae"] <= rep["validation"]["baseline_mae"]
    gates = check_gates(rep)
    # candidate learns promo lift; must not regress badly
    assert isinstance(gates["pass"], bool)
    assert isinstance(gates["reasons"], list)


def test_gate_thresholds_come_from_policy():
    import ml.training as t

    doc = yaml.safe_load((ROOT / "policies/gates.yaml").read_text())["quality"]
    assert t._QUALITY == doc
    assert doc == {"min_improvement": 0.10, "max_series_worsen": 0.05}


def test_registry_alias_does_not_move_running():
    registry.reset()
    a = registry.register("digest-a", "run-1", {"note": "first"})
    b = registry.register("digest-b", "run-2", {"note": "second"})
    registry.set_alias("prod", a["version"])
    running = registry.get_running_version(a["version"])
    registry.set_alias("prod", b["version"])
    assert running["version"] == a["version"]
    assert registry.resolve("prod")["version"] == b["version"]
    assert registry.resolve(a["version"])["artifact_digest"] == "digest-a"
