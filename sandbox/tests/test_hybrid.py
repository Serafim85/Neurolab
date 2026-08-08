"""D4 hybrid bio-front → silicon SNN."""

from __future__ import annotations

import json
from pathlib import Path

from closed_sandbox.cli import main
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import ManifestError, load_project
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "hybrid_ecg_snn_v0" / "project.toml"


def test_hybrid_run() -> None:
    project = load_project(EXAMPLE)
    assert project["project"]["domain"] == "hybrid"
    metrics = run_project(project, seed=42)
    assert metrics["hybrid_front"] == "synthetic_ecg_v0"
    assert metrics["hybrid_backend"] == "snn_lif"
    assert "→" in metrics["hybrid_pipeline"]
    assert 0.0 <= metrics["f1"] <= 1.0
    assert "digital hybrid" in metrics["hybrid_disclaimer"]
    assert metrics["budget_ok"] is True


def test_hybrid_eeg_front() -> None:
    project = load_project(EXAMPLE)
    project["front"]["kind"] = "synthetic_eeg_v0"
    metrics = run_project(project, seed=3)
    assert metrics["hybrid_front"] == "synthetic_eeg_v0"


def test_hybrid_bad_backend() -> None:
    project = load_project(EXAMPLE)
    project["backend"]["kind"] = "loihi_runtime"
    from closed_sandbox.domains import hybrid

    with pytest.raises(ManifestError, match="backend"):
        hybrid.validate_project(project)


def test_hybrid_cli(tmp_path: Path) -> None:
    out = tmp_path / "out"
    try:
        main(["run", str(EXAMPLE), "--out", str(out), "--seed", "42"])
    except SystemExit as exc:
        assert exc.code in (0, 2), exc.code
    data = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert data["domain"] == "hybrid"
    assert (out / "report.md").is_file()
