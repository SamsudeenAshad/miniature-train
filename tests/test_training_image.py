"""Training image tests (Step 78). Image matches WorkflowTemplate invocation."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_training_image_matches_workflow():
    df = (ROOT / "infra/docker/training.Dockerfile").read_text()
    assert df.startswith("FROM python:3.13-slim")
    assert 'ENTRYPOINT ["python", "-m", "workers.training.runner"]' in df
    wf = yaml.safe_load((ROOT / "infra/workflows/training-dag.yaml").read_text())
    step = next(t for t in wf["spec"]["templates"] if t["name"] == "step")
    assert step["container"]["command"] == ["python", "-m", "workers.training.runner"]
    assert step["container"]["image"].startswith("miniature-train/training:")
