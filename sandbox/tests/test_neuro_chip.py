"""D1 neuro_chip estimate domain."""

from __future__ import annotations

import json
from pathlib import Path

from closed_sandbox.cli import main
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import ManifestError, load_project
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "chip_estimate_v0" / "project.toml"


def test_neuro_chip_run_with_source() -> None:
    project = load_project(EXAMPLE)
    assert project["project"]["domain"] == "neuro_chip"
    metrics = run_project(project, seed=42)
    assert metrics["chip_target"] == "generic_neuromorphic_v0"
    assert metrics["chip_estimate_kind"] == "from_source_metrics"
    assert metrics["spike_count"] == 328
    assert metrics["synops"] == 6057
    assert metrics["f1"] == 0.8947
    assert "chip_area_mm2" in metrics
    assert "chip_power_mw" in metrics
    assert 0.0 <= metrics["chip_fit_score"] <= 1.0
    assert metrics["budget_ok"] is True
    assert "not silicon" in metrics["chip_estimate_disclaimer"]


def test_neuro_chip_topology_heuristic(tmp_path: Path) -> None:
    toml = tmp_path / "project.toml"
    toml.write_text(
        """
[project]
id = "chip-topo"
domain = "neuro_chip"

[network]
kind = "neuro_chip"
n_inputs = 8
n_hidden = 32
n_outputs = 2

[chip]
target = "generic_neuromorphic_v0"

[budget]
max_neurons = 128
max_synapses = 4096
max_spikes_per_sample = 5000
max_chip_power_mw = 50.0
max_chip_area_mm2 = 25.0

[task]
metric_primary = "chip_fit_score"
""",
        encoding="utf-8",
    )
    project = load_project(toml)
    metrics = run_project(project, seed=0)
    assert metrics["chip_estimate_kind"] == "topology_heuristic"
    assert metrics["n_neurons"] == 34  # 32+2
    assert metrics["n_synapses"] == 8 * 32 + 32 * 2


def test_neuro_chip_bad_target() -> None:
    project = load_project(EXAMPLE)
    project["chip"]["target"] = "loihi_fantasy"
    from closed_sandbox.domains import neuro_chip

    with pytest.raises(ManifestError, match="target"):
        neuro_chip.validate_project(project)


def test_neuro_chip_cli(tmp_path: Path) -> None:
    out = tmp_path / "out"
    try:
        main(["run", str(EXAMPLE), "--out", str(out), "--seed", "42"])
    except SystemExit as exc:
        assert exc.code in (0, 2), exc.code
    data = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert data["domain"] == "neuro_chip"
    assert data["chip_target"] == "generic_neuromorphic_v0"
    assert (out / "report.md").is_file()


FPGA = ROOT / "examples" / "chip_fpga_lite_v0" / "project.toml"


def test_fpga_snn_lite_run_and_export(tmp_path: Path) -> None:
    project = load_project(FPGA)
    metrics = run_project(project, seed=42)
    assert metrics["chip_target"] == "fpga_snn_lite_v0"
    assert metrics["chip_class"] == "fpga"
    assert metrics["chip_luts_est"] > 0
    assert "chip_export" in metrics
    assert metrics["chip_export"]["schema"] == "fpga_snn_lite_v0.export.v1"
    assert metrics["budget_ok"] is True

    out = tmp_path / "out"
    try:
        main(["run", str(FPGA), "--out", str(out), "--seed", "42"])
    except SystemExit as exc:
        assert exc.code in (0, 2), exc.code
    export_path = out / "chip_export.json"
    assert export_path.is_file()
    export = json.loads(export_path.read_text(encoding="utf-8"))
    assert export["resource_proxy"]["luts_est"] == metrics["chip_luts_est"]


def test_list_targets_includes_fpga() -> None:
    from closed_sandbox.domains.neuro_chip import list_targets

    assert "fpga_snn_lite_v0" in list_targets()
    assert "generic_neuromorphic_v0" in list_targets()
