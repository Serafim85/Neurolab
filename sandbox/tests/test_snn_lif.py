from __future__ import annotations

from pathlib import Path

from closed_sandbox.engine import run_project
from closed_sandbox.manifest import load_project
from closed_sandbox.report import diff_metrics, write_json

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "anomaly_v0" / "project.toml"


def test_load_and_run_example() -> None:
    project = load_project(EXAMPLE)
    assert project["project"]["domain"] == "snn_lif"
    metrics = run_project(project, seed=42)
    assert "f1" in metrics
    assert "spike_count" in metrics
    assert "synops" in metrics
    assert "latency_proxy_ms" in metrics
    assert metrics["budget_ok"] is True
    assert metrics["n_test"] == 42  # 14 per scenario × 3
    assert metrics["f1"] >= 0.70
    assert metrics["accuracy"] >= 0.65
    assert "wall_ms" in metrics
    assert metrics["wall_ms"] > 0


def test_by_scenario_metrics_differ() -> None:
    project = load_project(EXAMPLE)
    metrics = run_project(project, seed=42)
    by = metrics["by_scenario"]
    assert set(by) == {"nominal", "anomaly", "noise"}
    for name, row in by.items():
        assert row["n"] == 14
        assert "f1" in row and "accuracy" in row
        assert "spike_count" in row and "synops" in row
    # Generative conditions should not collapse to identical rows.
    triples = {
        (by[n]["f1"], by[n]["spike_count"], by[n]["synops"]) for n in by
    }
    assert len(triples) >= 2, "expected at least two distinct scenario metric rows"


def test_diff_metrics(tmp_path: Path) -> None:
    project = load_project(EXAMPLE)
    a = run_project(project, seed=42)
    b = run_project(project, seed=43)
    write_json(a, tmp_path / "a.json")
    write_json(b, tmp_path / "b.json")
    result = diff_metrics(a, b)
    assert "changed" in result
    assert result["n_changed"] >= 1
