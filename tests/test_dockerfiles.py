"""Dockerfile tests (Step 72)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "infra/docker"


def test_images_pinned_nonroot_runnable():
    reqs = (ROOT.parents[1] / "requirements.txt").read_text()
    assert "uvicorn==" in reqs
    for f in ("control-api.Dockerfile", "inference.Dockerfile"):
        body = (ROOT / f).read_text()
        assert body.startswith("FROM python:3.13-slim")
        assert "USER 65532:65532" in body
        assert "uvicorn" in body and "--app-dir" in body
        assert "services.control-api.app" not in body and "services.inference.app" not in body
