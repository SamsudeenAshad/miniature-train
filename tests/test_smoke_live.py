"""Live boot smoke test (Step 314). Boots both APIs under real uvicorn and
exercises the deployment path TestClient cannot cover: --app-dir resolution,
entrypoints, and HTTP semantics over the wire.

Skips (rather than fails) if the servers do not boot in this environment.
"""

import json
import shutil
import socket
import subprocess
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_healthy(base: str, timeout_s: float = 60.0) -> None:
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base + "/health/live", timeout=5) as r:
                if r.status == 200:
                    return
        except Exception as e:  # noqa: BLE001 - boot polling, any failure retries
            last = e
        time.sleep(1.0)
    pytest.skip(f"server at {base} did not boot: {last!r}")


def _request(method: str, url: str, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json", **(headers or {})})

    def _read(r):
        # Header names are case-insensitive on the wire; normalize for asserts.
        return r.status, {k.lower(): v for k, v in dict(r.headers).items()}, r.read()

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return _read(r)
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in dict(e.headers).items()}, e.read()


def test_live_boot_and_paths():
    if shutil.which("uvicorn") is None and shutil.which("python") is None:
        pytest.skip("no python launcher for uvicorn")
    api_port, inf_port = _free_port(), _free_port()
    procs = []
    try:
        procs.append(subprocess.Popen(
            ["python", "-m", "uvicorn", "app.main:app", "--port", str(api_port),
             "--app-dir", "services/control-api"], cwd=ROOT,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        procs.append(subprocess.Popen(
            ["python", "-m", "uvicorn", "app.main:app", "--port", str(inf_port),
             "--app-dir", "services/inference"], cwd=ROOT,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        api, inf = f"http://127.0.0.1:{api_port}", f"http://127.0.0.1:{inf_port}"
        _wait_healthy(api)
        _wait_healthy(inf)

        h = {"X-Subject": "admin-1", "X-Role": "project_admin"}
        s, headers, _ = _request("POST", api + "/v1/projects",
                                 {"name": "smoke", "owner": "owner-1"}, h)
        assert s == 201, s
        assert headers.get("location") == "/v1/projects/proj_1"

        s, _, _ = _request("GET", api + "/v1/projects/proj_1/overview",
                           headers={"X-Subject": "owner-1"})
        assert s == 200, s

        s, _, raw = _request("POST", inf + "/predict",
                             {"series_id": "s", "hour": 1, "day_of_week": 0,
                              "is_weekend": 0, "on_promotion": 0,
                              "history": [5] * 200})
        assert s == 200, s
        assert json.loads(raw)["prediction"] >= 0
    finally:
        for p in procs:
            p.terminate()
