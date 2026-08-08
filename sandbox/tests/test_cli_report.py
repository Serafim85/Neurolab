"""CLI run/diff and report writers (no Outpost)."""

from __future__ import annotations

import json
from pathlib import Path

from closed_sandbox.cli import main
from closed_sandbox.report import (
    diff_metrics,
    load_metrics_json,
    write_json,
    write_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "anomaly_v0" / "project.toml"


def test_write_and_diff_report(tmp_path: Path) -> None:
    a = {
        "project_id": "anomaly-v0",
        "domain": "snn_lif",
        "f1": 0.9,
        "spike_count": 300,
        "synops": 1000,
        "budget_ok": True,
        "metric_primary": "f1",
    }
    b = {**a, "f1": 0.8, "spike_count": 350}
    write_json(a, tmp_path / "a.json")
    write_markdown(a, tmp_path / "a.md")
    md = (tmp_path / "a.md").read_text(encoding="utf-8")
    assert "f1" in md
    assert "Resource economy" in md
    assert "quality_per_kspike" in md
    loaded = load_metrics_json(tmp_path / "a.json")
    assert loaded["f1"] == 0.9
    assert loaded["quality_per_kspike"] == round(1000.0 * 0.9 / 300.0, 6)
    assert loaded["quality_per_ksynop"] == round(1000.0 * 0.9 / 1000.0, 6)
    diff = diff_metrics(a, b)
    assert diff["n_changed"] >= 2
    assert abs(diff["changed"]["f1"]["delta"] - (-0.1)) < 1e-9


def test_cli_run_and_diff(tmp_path: Path, capsys) -> None:
    out = tmp_path / "out"
    try:
        main(["run", str(EXAMPLE), "--out", str(out), "--seed", "42"])
    except SystemExit as exc:
        assert exc.code in (0, 2), exc.code
    metrics_path = out / "metrics.json"
    assert metrics_path.is_file()
    assert (out / "report.md").is_file()
    data = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert data["domain"] == "snn_lif"
    assert "f1" in data
    assert data["budget_ok"] is True
    assert "wall_ms" in data

    try:
        main(["diff", str(metrics_path), str(metrics_path)])
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr().out
    assert '"n_changed": 0' in captured or '"n_changed":0' in captured.replace(" ", "")


def test_cli_stress_small(tmp_path: Path) -> None:
    out = tmp_path / "stress"
    try:
        main(
            [
                "stress",
                str(EXAMPLE),
                "--n-seeds",
                "3",
                "--seeds-from",
                "40",
                "--out",
                str(out),
                "--min-mean-f1",
                "0.5",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 0, exc.code
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["n_seeds"] == 3
    assert (out / "report.md").is_file()
    assert (out / "seed-40.json").is_file()
