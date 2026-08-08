"""Outpost lifecycle helpers for Closed Sandbox integration tests."""

from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path

NEUROLAB_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = NEUROLAB_ROOT / "config" / "sovereign.sandbox-ask.toml"
DEFAULT_GGUF = NEUROLAB_ROOT / "artifacts" / "outpost-tiny-hammer.Q4_K_M.gguf"
DEFAULT_PORT = 8098


def commercial_sovereignd() -> Path | None:
    commercial = Path(
        os.environ.get(
            "COMMERCIAL", str(Path.home() / "Projects" / "AI-Platform-Vision")
        )
    )
    for rel in ("target/release/sovereignd", "target/debug/sovereignd"):
        cand = commercial / rel
        if cand.is_file() and os.access(cand, os.X_OK):
            return cand
    return None


def port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def wait_health(base_url: str, *, timeout_s: float = 180.0) -> dict:
    health_url = base_url.rstrip("/") + "/health"
    deadline = time.time() + timeout_s
    last_err = ""
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health_url, timeout=2) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = str(exc)
            time.sleep(0.5)
    raise TimeoutError(f"Outpost health not ready at {health_url}: {last_err}")


def outpost_ready_reason() -> str | None:
    """Return skip reason if integration cannot run, else None."""
    if commercial_sovereignd() is None:
        return (
            "sovereignd binary not found under "
            "AI-Platform-Vision/target/{release,debug}"
        )
    if not DEFAULT_GGUF.is_file():
        return f"missing GGUF: {DEFAULT_GGUF}"
    if not DEFAULT_CONFIG.is_file():
        return f"missing config: {DEFAULT_CONFIG}"
    return None
