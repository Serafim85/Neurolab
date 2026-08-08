"""CS-P05 Ask UI API — unit, no live Outpost required for banner/errors."""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from pathlib import Path
from unittest.mock import patch

import pytest

from closed_sandbox.ui_server import Handler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "anomaly_v0" / "project.toml"
METRICS = ROOT / "examples" / "anomaly_v0" / "out" / "seed42" / "metrics.json"


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


def test_ask_page_and_health(ui_server: int) -> None:
    status, health = _get(ui_server, "/api/health")
    assert status == 200
    assert "CS-P05" in health["screens"]

    status, html = _get(ui_server, "/ask")
    assert status == 200
    assert "Ask assistant" in html
    assert "FR-UI-030" in html
    assert 'id="banner-public"' in html
    assert "WARNING" in html


def test_project_exposes_contour(ui_server: int) -> None:
    status, info = _get(
        ui_server, f"/api/project?path={EXAMPLE.as_posix()}"
    )
    assert status == 200
    assert info["contour"]["provider"] == "local"
    assert info["contour"]["ask_enabled"] is True


def test_ask_api_mocked(ui_server: int) -> None:
    assert METRICS.is_file(), "seed42 metrics missing — run demo seeds first"
    with patch(
        "closed_sandbox.ui_server.ask",
        return_value="budget_ok is true for this run.",
    ) as mocked:
        status, result = _post_json(
            ui_server,
            "/api/ask",
            {
                "project": str(EXAMPLE),
                "metrics": str(METRICS),
                "question": "State whether budget_ok is true.",
                "provider": "local",
            },
        )
    assert status == 200, result
    assert result["ok"] is True
    assert result["provider"] == "local"
    assert result["risk_banner"] is False
    assert "budget_ok" in result["answer"]
    mocked.assert_called_once()


def test_ask_public_banner_flag(ui_server: int, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLOSED_SANDBOX_LLM_API_KEY", "test-key-not-used")
    with patch(
        "closed_sandbox.ui_server.ask",
        return_value="WARNING: provider=public — leave machine.\nAnswer body.",
    ):
        status, result = _post_json(
            ui_server,
            "/api/ask",
            {
                "project": "examples/anomaly_v0/project.toml",
                "metrics": "examples/anomaly_v0/out/seed42/metrics.json",
                "question": "ping",
                "provider": "public",
            },
        )
    assert status == 200, result
    assert result["provider"] == "public"
    assert result["risk_banner"] is True
    assert result["warning"]
    assert result["answer"] == "Answer body."


def test_ask_empty_question(ui_server: int) -> None:
    status, data = _post_json(
        ui_server,
        "/api/ask",
        {"project": str(EXAMPLE), "question": "  "},
    )
    assert status == 400
    assert data["ok"] is False
