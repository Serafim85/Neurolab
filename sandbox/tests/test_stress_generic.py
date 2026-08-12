"""Stress CLI on generic (non-spiking) domains — no KeyError on f1/spike_count."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import fixture_domains as fx
from closed_sandbox.cli import main

ROOT = Path(__file__).resolve().parents[1]
BIOCOMPUTE = ROOT / "examples" / "biocompute_grn_v0" / "project.toml"
ANOMALY = ROOT / "examples" / "anomaly_v0" / "project.toml"


def _write_cost_probe_project(path: Path) -> Path:
    proj = path / "project.toml"
    proj.write_text(
        "\n".join(
            [
                "[project]",
                'id = "cost-probe-stress"',
                'domain = "cost_probe_test"',
                "",
                "[estimate]",
                "unit_cost_eur = 12.5",
                "",
                "[budget]",
                "max_unit_cost_eur = 50.0",
                "",
                "[sandbox]",
                "seed = 7",
                'scenarios = ["baseline"]',
                "",
                "[economy]",
                'cost_key = "unit_cost_eur"',
                'cost_unit = "EUR"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return proj


def test_stress_generic_fixture(register_domain, tmp_path: Path) -> None:
    register_domain(fx.COST_PROBE)
    proj = _write_cost_probe_project(tmp_path)
    out = tmp_path / "stress"
    try:
        main(
            [
                "stress",
                str(proj),
                "--n-seeds",
                "2",
                "--seeds-from",
                "0",
                "--out",
                str(out),
                "--min-primary",
                "0.5",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 0, exc.code
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["metric_primary"] == "fit_score"
    assert "fit_score_mean" in summary
    assert "f1_mean" not in summary
    assert "spike_count_mean" not in summary
    report = (out / "report.md").read_text(encoding="utf-8")
    assert "fit_score" in report
    assert "spike_count" not in report


def test_stress_biocompute(tmp_path: Path) -> None:
    out = tmp_path / "stress"
    try:
        main(
            [
                "stress",
                str(BIOCOMPUTE),
                "--n-seeds",
                "2",
                "--seeds-from",
                "0",
                "--out",
                str(out),
                "--min-primary",
                "0.0",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 0, exc.code
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["metric_primary"] == "accuracy"
    assert "accuracy_mean" in summary
    assert (out / "report.md").is_file()


def test_stress_min_mean_f1_alias(tmp_path: Path, capsys) -> None:
    out = tmp_path / "stress"
    try:
        main(
            [
                "stress",
                str(ANOMALY),
                "--n-seeds",
                "1",
                "--seeds-from",
                "42",
                "--out",
                str(out),
                "--min-mean-f1",
                "0.0",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 0, exc.code
    err = capsys.readouterr().err
    assert "deprecated" in err.lower()
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["metric_primary"] == "f1"
    assert "f1_mean" in summary
