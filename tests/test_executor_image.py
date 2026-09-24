"""Executor image tests (Step 79)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "infra/docker"


def test_executor_image_minimal():
    df = (ROOT / "executor.Dockerfile").read_text()
    assert df.startswith("FROM python:3.13-slim")
    assert "USER 65532:65532" in df
    assert "COPY workers/executor workers/executor" in df
