"""Model card / bundle tests."""

from ml.cards import evaluation_bundle, model_card
from ml.data_generator import generate_rows
from ml.features import fit_preprocessing
from ml.training import check_gates, train_and_evaluate


def test_card_and_bundle():
    rows = generate_rows(seed=42)
    rep = train_and_evaluate(rows, seed=42, train_mean=fit_preprocessing(rows)["train_mean"])
    card = model_card("run-1", "digest-x", "demand-features-1.0", rep["validation"])
    assert len(card["digest"]) == 64
    bundle = evaluation_bundle(rep, check_gates(rep))
    assert bundle["schema_version"] == "eval-bundle-1.0"
    assert bundle["artifact_digest"] == rep["artifact_digest"]
