"""CS-P01 Overview + CS-P02 Editor UI API."""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from closed_sandbox.ui_server import Handler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = "examples/anomaly_v0/project.toml"


@pytest.fixture()
def ui_server():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield port
    finally:
        httpd.shutdown()
        httpd.server_close()


def _get(port: int, path: str) -> tuple[int, dict | str]:
    conn = HTTPConnection("127.0.0.1", port, timeout=60)
    conn.request("GET", path)
    resp = conn.getresponse()
    body = resp.read().decode("utf-8")
    ctype = resp.getheader("Content-Type") or ""
    if "json" in ctype:
        return resp.status, json.loads(body)
    return resp.status, body


def _post_json(port: int, path: str, payload: dict) -> tuple[int, dict]:
    conn = HTTPConnection("127.0.0.1", port, timeout=120)
    raw = json.dumps(payload).encode("utf-8")
    conn.request(
        "POST",
        path,
        body=raw,
        headers={"Content-Type": "application/json", "Content-Length": str(len(raw))},
    )
    resp = conn.getresponse()
    return resp.status, json.loads(resp.read().decode("utf-8"))


def test_overview_page_and_projects(ui_server: int) -> None:
    status, health = _get(ui_server, "/api/health")
    assert status == 200
    assert "CS-P01" in health["screens"]
    assert "CS-P02" in health["screens"]

    status, html = _get(ui_server, "/")
    assert status == 200
    assert "Projects" in html
    assert "FR-UI-001" in html

    status, data = _get(ui_server, "/api/projects")
    assert status == 200
    assert data["ok"] is True
    assert data["n"] >= 6
    ids = {p["id"] for p in data["projects"]}
    assert "anomaly-v0" in ids


def test_editor_page_manifest_validate(ui_server: int) -> None:
    status, html = _get(ui_server, "/editor")
    assert status == 200
    assert "FR-UI-002" in html

    status, man = _get(ui_server, f"/api/manifest?path={EXAMPLE}")
    assert status == 200
    assert man["ok"] is True
    assert "anomaly-v0" in man["toml"]
    assert man["project"]["domain"] == "snn_lif"

    status, ok = _post_json(
        ui_server,
        "/api/validate",
        {"project": EXAMPLE, "toml": man["toml"]},
    )
    assert status == 200
    assert ok["valid"] is True

    bad = man["toml"].replace("n_outputs = 2", "n_outputs = 1")
    status, fail = _post_json(
        ui_server,
        "/api/validate",
        {"project": EXAMPLE, "toml": bad},
    )
    assert status == 400
    assert fail["valid"] is False
    assert fail["error"]
