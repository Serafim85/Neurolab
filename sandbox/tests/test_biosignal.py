"""D3 biosignal synthetic ECG/EEG."""

from __future__ import annotations

import json
from pathlib import Path

from closed_sandbox.cli import main
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import ManifestError, load_project
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "biosignal_ecg_v0" / "project.toml"


def test_biosignal_ecg_run() -> None:
    project = load_project(EXAMPLE)
    assert project["project"]["domain"] == "biosignal"
    metrics = run_project(project, seed=42)
    assert metrics["signal_kind"] == "synthetic_ecg_v0"
    assert metrics["signal_encode"] == "threshold"
    assert metrics["spike_count"] >= 0
    assert 0.0 <= metrics["f1"] <= 1.0
    assert "not clinical" in metrics["signal_disclaimer"]
    assert metrics["budget_ok"] is True


def test_biosignal_eeg_kind() -> None:
    project = load_project(EXAMPLE)
    project["signal"]["kind"] = "synthetic_eeg_v0"
    metrics = run_project(project, seed=7)
    assert metrics["signal_kind"] == "synthetic_eeg_v0"
    assert metrics["budget_ok"] is True


def test_biosignal_bad_kind() -> None:
    project = load_project(EXAMPLE)
    project["signal"]["kind"] = "clinical_holter"
    from closed_sandbox.domains import biosignal

    with pytest.raises(ManifestError, match="kind"):
        biosignal.validate_project(project)


def test_biosignal_cli(tmp_path: Path) -> None:
    out = tmp_path / "out"
    try:
        main(["run", str(EXAMPLE), "--out", str(out), "--seed", "42"])
    except SystemExit as exc:
        assert exc.code in (0, 2), exc.code
    data = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert data["domain"] == "biosignal"
    assert (out / "report.md").is_file()
