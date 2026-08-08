"""CS-P03 UI API (stdlib server) — unit, no browser."""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from closed_sandbox.ui_server import Handler, SANDBOX_ROOT, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "anomaly_v0" / "project.toml"


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


def test_health_and_static(ui_server: int) -> None:
    status, data = _get(ui_server, "/api/health")
    assert status == 200
    assert data["ok"] is True
    assert "CS-P03" in data.get("screens", []) or "CS-P03" in str(data.get("ui", ""))
    assert Path(data["sandbox_root"]) == SANDBOX_ROOT

    status, html = _get(ui_server, "/run")
    assert status == 200
    assert "Run + Results" in html
    assert "FR-UI-010" in html


def test_project_and_run_export(ui_server: int) -> None:
    status, info = _get(
        ui_server, f"/api/project?path={EXAMPLE.as_posix()}"
    )
    assert status == 200
    assert info["ok"] is True
    assert info["project"]["id"] == "anomaly-v0"
    assert "nominal" in info["scenarios"]

    out = ROOT / "examples" / "anomaly_v0" / "out" / "ui-test"
    status, result = _post_json(
        ui_server,
        "/api/run",
        {"project": str(EXAMPLE), "seed": 42, "out": str(out)},
    )
    assert status == 200, result
    assert result["ok"] is True
    assert result["metrics"]["budget_ok"] is True
    assert "f1" in result["metrics"]
    by = result["metrics"]["by_scenario"]
    assert set(by) == {"nominal", "anomaly", "noise"}
    assert by["nominal"]["n"] == 14
    assert (out / "metrics.json").is_file()
    assert (out / "report.md").is_file()
    report_text = (out / "report.md").read_text(encoding="utf-8")
    assert "## Per scenario" in report_text
    assert "| nominal |" in report_text

    status, metrics_body = _get(ui_server, "/api/export/metrics.json")
    assert status == 200
    assert isinstance(metrics_body, dict)
    assert "f1" in metrics_body

    status, md = _get(ui_server, "/api/export/report.md")
    assert status == 200
    assert isinstance(md, str)
    assert "Sandbox report" in md


def test_reject_path_outside_sandbox(ui_server: int) -> None:
    status, data = _get(ui_server, "/api/project?path=/etc/passwd")
    assert status == 400
    assert data["ok"] is False
    assert "under" in data["error"].lower() or "not found" in data["error"].lower()
