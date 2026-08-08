"""Shared fixtures for Closed Sandbox tests."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from outpost_util import (
    DEFAULT_CONFIG,
    DEFAULT_PORT,
    commercial_sovereignd,
    outpost_ready_reason,
    port_open,
    wait_health,
)


@pytest.fixture(scope="session")
def outpost_base_url():
    """Boot sovereignd+hammer2 on :8098 or reuse if already healthy."""
    reason = outpost_ready_reason()
    if reason:
        pytest.skip(reason)

    base = f"http://127.0.0.1:{DEFAULT_PORT}"
    proc: subprocess.Popen[bytes] | None = None
    started_here = False
    log_f = None

    if port_open("127.0.0.1", DEFAULT_PORT):
        try:
            wait_health(base, timeout_s=5)
        except TimeoutError:
            pytest.skip(f"port {DEFAULT_PORT} busy but /health not responding")
    else:
        binary = commercial_sovereignd()
        assert binary is not None
        log_path = Path("/tmp/sandbox-ask-sovereignd-pytest.log")
        log_f = log_path.open("wb")
        neurolab_root = Path(__file__).resolve().parents[2]
        proc = subprocess.Popen(
            [str(binary), str(DEFAULT_CONFIG)],
            cwd=str(neurolab_root),
            stdout=log_f,
            stderr=subprocess.STDOUT,
        )
        started_here = True
        try:
            wait_health(
                base,
                timeout_s=float(os.environ.get("OUTPOST_BOOT_TIMEOUT", "180")),
            )
        except TimeoutError:
            if log_f is not None:
                log_f.flush()
            tail = ""
            if log_path.is_file():
                tail = log_path.read_text(encoding="utf-8", errors="replace")[-2000:]
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=10)
            if log_f is not None:
                log_f.close()
            pytest.skip("sovereignd failed to become healthy:\n" + tail)

    yield base + "/v1"

    if started_here and proc is not None:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
    if log_f is not None:
        log_f.close()
