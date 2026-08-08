"""D2 biocompute digital GRN."""

from __future__ import annotations

import json
from pathlib import Path

from closed_sandbox.cli import main
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import ManifestError, load_project
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "biocompute_grn_v0" / "project.toml"


def test_biocompute_run() -> None:
    project = load_project(EXAMPLE)
    assert project["project"]["domain"] == "biocompute"
    metrics = run_project(project, seed=42)
    assert metrics["bio_kind"] == "boolean_grn_v0"
    assert metrics["spike_count"] == 0
    assert metrics["bio_n_genes"] == 12
    assert metrics["bio_resource_proxy"] > 0
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert "not wet-lab" in metrics["bio_disclaimer"]
    assert metrics["budget_ok"] is True


def test_biocompute_bad_kind() -> None:
    project = load_project(EXAMPLE)
    project["circuit"]["kind"] = "organoid_farm"
    from closed_sandbox.domains import biocompute

    with pytest.raises(ManifestError, match="kind"):
        biocompute.validate_project(project)


def test_biocompute_cli(tmp_path: Path) -> None:
    out = tmp_path / "out"
    try:
        main(["run", str(EXAMPLE), "--out", str(out), "--seed", "42"])
    except SystemExit as exc:
        assert exc.code in (0, 2), exc.code
    data = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert data["domain"] == "biocompute"
    assert (out / "report.md").is_file()
