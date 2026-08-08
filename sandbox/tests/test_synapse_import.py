from __future__ import annotations

import json
from pathlib import Path

from closed_sandbox.cli import main
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import load_project

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "synapse_e5_import" / "project.toml"


def test_synapse_import_run() -> None:
    project = load_project(EXAMPLE)
    assert project["project"]["domain"] == "synapse_import"
    metrics = run_project(project, seed=0)
    assert metrics["accuracy"] == 0.8636
    assert metrics["escalate_rate"] == 0.0682
    assert metrics["budget_ok"] is True
    assert metrics["spike_count"] == 0
    assert "e5-official.json" in metrics["import_source"]


def test_synapse_import_cli(tmp_path: Path) -> None:
    out = tmp_path / "out"
    try:
        main(["run", str(EXAMPLE), "--out", str(out)])
    except SystemExit as exc:
        assert exc.code == 0, exc.code
    data = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert data["synapse_pack"] == "e5-brain-escalate"
    assert (out / "report.md").is_file()
