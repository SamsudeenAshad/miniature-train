"""Control API skeleton (SRS 8.2, FR-001/FR-002). Full auth/z in WBS 2.3."""

from fastapi import FastAPI

app = FastAPI(title="miniature-train control API", version="0.1.0")


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready", "deps": "skeleton"}
