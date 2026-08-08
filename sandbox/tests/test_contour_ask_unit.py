"""Unit tests for contour_ask without a live daemon."""

from __future__ import annotations

import pytest

from closed_sandbox.contour_ask import AskError, ask


def _project(**contour_over: object) -> dict:
    contour = {
        "ask_enabled": True,
        "provider": "local",
        "base_url": "http://127.0.0.1:8098/v1",
        "model": "outpost-tiny-hammer",
        "api_key_env": "CLOSED_SANDBOX_LLM_API_KEY",
    }
    contour.update(contour_over)
    return {
        "project": {"id": "t", "domain": "snn_lif"},
        "network": {"kind": "snn_lif"},
        "contour": contour,
    }


def test_ask_disabled() -> None:
    with pytest.raises(AskError, match="disabled"):
        ask(_project(ask_enabled=False), {"f1": 0.9}, "hi")


def test_ask_unknown_provider() -> None:
    with pytest.raises(AskError, match="unknown"):
        ask(_project(provider="spaceship"), {"f1": 0.9}, "hi")


def test_ask_public_requires_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CLOSED_SANDBOX_LLM_API_KEY", raising=False)
    with pytest.raises(AskError, match="CLOSED_SANDBOX_LLM_API_KEY"):
        ask(
            _project(provider="public", base_url="https://api.openai.com/v1"),
            {"f1": 0.9},
            "hi",
        )


def test_ask_local_unreachable() -> None:
    # Port unlikely to host Outpost; should fail with clear AskError
    with pytest.raises(AskError, match="cannot reach|HTTP"):
        ask(
            _project(base_url="http://127.0.0.1:59999/v1"),
            {"f1": 0.9, "budget_ok": True},
            "ping",
        )
