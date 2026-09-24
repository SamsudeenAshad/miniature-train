"""Model cards + evaluation reports (FR-009/011 slice, WBS 4.2/10.2)."""

from __future__ import annotations

import hashlib
import json
import time


def model_card(run_id: str, dataset_digest: str, feature_version: str, metrics: dict, owner: str = "ml-team") -> dict:
    card = {
        "run_id": run_id,
        "dataset_digest": dataset_digest,
        "feature_version": feature_version,
        "metrics": metrics,
        "owner": owner,
        "validation_status": "pending",
        "generated_at": time.time(),
    }
    card["digest"] = hashlib.sha256(json.dumps(card, sort_keys=True, default=str).encode()).hexdigest()
    return card


def evaluation_bundle(report: dict, gates: dict, benchmark: dict | None = None) -> dict:
    return {
        "generated_at": time.time(),
        "schema_version": "eval-bundle-1.0",
        "metrics": report.get("validation"),
        "gates": gates,
        "benchmark": benchmark or {},
        "artifact_digest": report.get("artifact_digest"),
    }
