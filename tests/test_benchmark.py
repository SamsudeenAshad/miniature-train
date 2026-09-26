"""Benchmark scoring tests (ML-004/005 slice)."""

from workers.aiops.benchmark import FAULT_FAMILIES, diagnosis_score, match
from workers.aiops.harness import FAMILIES


def test_families_single_sourced():
    assert FAULT_FAMILIES == FAMILIES == ("cpu", "memory", "latency", "errors", "faulty_deploy")


def test_event_matching_one_to_one():
    eps = [{"id": "e1", "service_group": "api", "start": 100, "end": 400},
           {"id": "e2", "service_group": "api", "start": 1000, "end": 1300}]
    incs = [{"service_group": "api", "ts": 150}, {"service_group": "api", "ts": 160}, {"service_group": "db", "ts": 1100}]
    s = match(incs, eps)
    assert s["tp"] == 1 and s["fp"] == 2 and s["fn"] == 1
    assert s["delay_median_s"] == 50


def test_diagnosis_abstention_counts_as_miss():
    preds = [
        {"episode_id": "e1", "rank1": "api", "rank2": "db", "rank3": "x", "truth": "api"},
        {"episode_id": "e2", "abstained": True, "rank1": None, "rank2": None, "rank3": None, "truth": "db"},
    ]
    d = diagnosis_score(preds, eligible=2)
    assert d["top1"] == 0.5 and d["top3"] == 0.5
