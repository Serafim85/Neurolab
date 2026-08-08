"""CS-P04 Diff UI API — unit, no browser."""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from closed_sandbox.engine import run_project
from closed_sandbox.manifest import load_project
from closed_sandbox.report import write_json
from closed_sandbox.ui_server import Handler, ThreadingHTTPServer

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


def test_diff_page_and_api(ui_server: int, tmp_path: Path) -> None:
    status, health = _get(ui_server, "/api/health")
    assert status == 200
    assert "CS-P04" in health["screens"]

    status, html = _get(ui_server, "/diff")
    assert status == 200
    assert "Diff versions" in html
    assert "FR-UI-020" in html

    out = tmp_path / "diff-ui"
    out.mkdir()
    project = load_project(EXAMPLE)
    # Write under sandbox tree (API path policy).
    dest = ROOT / "examples" / "anomaly_v0" / "out" / "ui-diff-test"
    dest.mkdir(parents=True, exist_ok=True)
    a = run_project(project, seed=42)
    b = run_project(project, seed=43)
    write_json(a, dest / "a.json")
    write_json(b, dest / "b.json")

    rel_a = "examples/anomaly_v0/out/ui-diff-test/a.json"
    rel_b = "examples/anomaly_v0/out/ui-diff-test/b.json"
    status, result = _post_json(
        ui_server, "/api/diff", {"a": rel_a, "b": rel_b}
    )
    assert status == 200, result
    assert result["ok"] is True
    assert result["n_changed"] >= 1
    assert "changed" in result["diff"]
    assert result["diff"]["n_changed"] == result["n_changed"]


def test_diff_rejects_outside_sandbox(ui_server: int) -> None:
    status, data = _post_json(
        ui_server, "/api/diff", {"a": "/etc/passwd", "b": "/etc/hosts"}
    )
    assert status == 400
    assert data["ok"] is False
