"""Demo walkthrough test (AT-25 slice)."""

from ml.demo import run


def test_demo_evidence_chain():
    ev = run(seed=42, subset=2000)
    assert ev["validation_status"] == "accepted"
    assert ev["inference"]["request_id"] == "req_demo"
    assert ev["model_version"] == 1
    assert "lineage" in ev
    assert isinstance(ev["gates"]["pass"], bool)
