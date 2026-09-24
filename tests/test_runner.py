"""Runner stage tests (Step 77, FR-007 slice)."""

from workers.training.runner import main, run_stage


def test_all_stages():
    assert run_stage("validate")["status"] == "accepted"
    assert len(run_stage("train")["artifact_digest"]) == 64
    assert "mae" in run_stage("evaluate")
    assert run_stage("register")["version"] == 1
    assert main(["--stage", "validate"])["status"] == "accepted"
