"""Web image tests (Step 101). Pinned multi-stage build ending non-root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "infra/docker"


def test_web_multistage():
    df = (ROOT / "web.Dockerfile").read_text()
    assert df.startswith("FROM node:22-slim AS build")
    assert "nginxinc/nginx-unprivileged:1.27-alpine" in df
    assert "USER nginx" in df
