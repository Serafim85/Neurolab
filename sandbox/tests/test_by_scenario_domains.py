"""by_scenario present for all domain examples (real split)."""

from __future__ import annotations

from pathlib import Path

import pytest

from closed_sandbox.engine import run_project
from closed_sandbox.manifest import load_project
from closed_sandbox.report import ensure_by_scenario

ROOT = Path(__file__).resolve().parents[1]

EXAMPLES = [
    ("anomaly_v0", {"nominal", "anomaly", "noise"}),
    ("chip_estimate_v0", {"nominal", "high_activity", "sparse"}),
    ("chip_fpga_lite_v0", {"nominal", "high_activity", "sparse"}),
    ("biocompute_grn_v0", {"balanced", "sparse", "dense"}),
    ("biosignal_ecg_v0", {"clean", "arrhythmia", "noisy"}),
    ("hybrid_ecg_snn_v0", {"clean", "arrhythmia", "noisy"}),
]


@pytest.mark.parametrize("name,keys", EXAMPLES)
def test_by_scenario_all_domains(name: str, keys: set[str]) -> None:
    project = load_project(ROOT / "examples" / name / "project.toml")
    metrics = run_project(project, seed=42)
    assert "by_scenario" in metrics
    assert set(metrics["by_scenario"]) == keys
    assert metrics.get("by_scenario_mode") == "split"
    for row in metrics["by_scenario"].values():
        assert "n" in row
        assert "spike_count" in row or "f1" in row or "accuracy" in row
    # Generative conditions should not collapse to identical rows.
    primary = metrics.get("metric_primary", "f1")
    triples = set()
    for row in metrics["by_scenario"].values():
        triples.add(
            (
                row.get(primary, row.get("f1", row.get("accuracy"))),
                row.get("spike_count"),
                row.get("synops"),
                row.get("chip_fit_score"),
            )
        )
    assert len(triples) >= 2, f"{name}: expected ≥2 distinct scenario rows"


def test_ensure_by_scenario_idempotent() -> None:
    metrics = {
        "f1": 0.9,
        "spike_count": 10,
        "synops": 100,
        "budget_ok": True,
        "by_scenario": {"x": {"n": 1, "f1": 0.9}},
        "by_scenario_mode": "split",
    }
    project = {"sandbox": {"scenarios": ["a", "b"]}}
    out = ensure_by_scenario(metrics, project)
    assert set(out["by_scenario"]) == {"x"}  # not overwritten
