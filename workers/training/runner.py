"""Trusted template runner (FR-007, WBS 4.1). One stage per Argo task invocation."""

from __future__ import annotations

import argparse
import json

STAGES = ("validate", "train", "evaluate", "register")


def run_stage(stage: str, seed: int = 42) -> dict:
    from ml.data_generator import generate_rows
    from ml.features import fit_preprocessing
    from ml.training import check_gates, train_and_evaluate
    from ml.validate import validate_rows

    rows = generate_rows(seed=seed)
    if stage == "validate":
        rep = validate_rows(rows)
        return {"stage": stage, "status": rep["status"], "rows": len(rows)}
    train_mean = fit_preprocessing(rows)["train_mean"]
    report = train_and_evaluate(rows, seed=seed, train_mean=train_mean)
    if stage == "train":
        return {"stage": stage, "artifact_digest": report["artifact_digest"]}
    if stage == "evaluate":
        return {"stage": stage, "mae": report["validation"]["mae"], "gates": check_gates(report)}
    if stage == "register":
        from ml import registry as reg

        reg.reset()
        entry = reg.register(report["artifact_digest"], run_id=f"run-seed-{seed}", model_card={"seed": seed})
        return {"stage": stage, "version": entry["version"]}
    raise ValueError(f"unknown_stage:{stage}")


def main(argv: list[str] | None = None) -> dict:
    ap = argparse.ArgumentParser(description="Trusted training stage runner")
    ap.add_argument("--stage", choices=STAGES, required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args(argv)
    result = run_stage(args.stage, seed=args.seed)
    print(json.dumps(result, default=str))
    return result


if __name__ == "__main__":
    main()
