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
    api = (ROOT / "control-api.Dockerfile").read_text()
    assert "COPY services/control-api services/control-api" in api
    assert "COPY ml ml" in api
    assert '"--app-dir", "services/control-api"' in api
    inf = (ROOT / "inference.Dockerfile").read_text()
    assert "COPY services/inference services/inference" in inf
    assert "COPY ml ml" in inf
    assert '"--app-dir", "services/inference"' in inf
