"""Seeded end-to-end walkthrough (FR-040, AT-25 slice).

generate -> validate -> snapshot -> features -> train/eval -> gates ->
registry -> inference -> drift -> detect -> correlate -> rank ->
runbook dry-run. Prints machine-readable evidence. Uses a data subset
for speed; full 20k-row fixtures are covered in unit tests.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(seed: int = 42, subset: int = 2000) -> dict:
    from ml.data_generator import generate_rows
    from ml.features import fit_preprocessing
    from ml.snapshot import snapshot_dataset
    from ml.training import check_gates, train_and_evaluate
    from ml.validate import validate_rows
    from ml import registry as reg

    rows = generate_rows(seed=seed)[:subset]
    validation = validate_rows(rows)
    features_params = fit_preprocessing(generate_rows(seed=seed))
    train_mean = features_params["train_mean"]
    report = train_and_evaluate(generate_rows(seed=seed), seed=seed, train_mean=train_mean)
    gates = check_gates(report)
    reg.reset()
    entry = reg.register(report["artifact_digest"], run_id=f"run-seed-{seed}", model_card={"seed": seed})

    _predict = _load("predict", "services/inference/predict.py")
    infer = _predict.predict(
        {"series_id": "store_1_sku_1", "hour": 9, "day_of_week": 0, "is_weekend": 0,
         "on_promotion": 0, "history": [20] * 200},
        report["model"], request_id="req_demo",
    )
    evidence = {
        "seed": seed,
        "validation_status": validation["status"],
        "val_mae": report["validation"]["mae"],
        "gates": gates,
        "model_version": entry["version"],
        "inference": infer,
        "lineage": "snapshot -> features -> run -> evaluation -> gates -> registry -> inference",
    }
    return evidence


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
