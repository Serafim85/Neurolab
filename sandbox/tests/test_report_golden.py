"""Golden files for `report.md` and `diff` output.

`report.md` is the artifact a customer is shown, so its exact shape is frozen
here. Volatile values (wall clock) are scrubbed; everything else is byte-exact
against `tests/golden/`.

Regenerate after an intentional format change:

    cd sandbox && PYTHONPATH=src:tests python tests/test_report_golden.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

import fixture_domains as fx
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import load_project
from closed_sandbox.report import (
    diff_metrics,
    load_metrics_json,
    write_json,
    write_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = Path(__file__).resolve().parent / "golden"
EXAMPLE = ROOT / "examples" / "anomaly_v0" / "project.toml"

FROZEN_A = GOLDEN / "anomaly_v0_metrics_seed42.json"
FROZEN_B = GOLDEN / "anomaly_v0_metrics_seed43.json"
REPORT_MD = GOLDEN / "anomaly_v0_report.md"
DIFF_JSON = GOLDEN / "anomaly_v0_diff.json"
GENERIC_MD = GOLDEN / "cost_probe_report.md"

# Wall clock depends on the machine; pin it so the golden stays comparable.
FROZEN_WALL_MS = 0.0


def _frozen_run(seed: int) -> dict[str, Any]:
    metrics = run_project(load_project(EXAMPLE), seed=seed)
    metrics["wall_ms"] = FROZEN_WALL_MS
    return metrics


def _frozen_cost_probe() -> dict[str, Any]:
    metrics = run_project(copy.deepcopy(fx.COST_PROBE_PROJECT))
    metrics["wall_ms"] = FROZEN_WALL_MS
    return metrics


def _rendered(metrics: dict[str, Any], tmp_path: Path) -> str:
    path = tmp_path / "report.md"
    write_markdown(metrics, path)
    return path.read_text(encoding="utf-8")


def _cli_diff(a: dict[str, Any], b: dict[str, Any], tmp_path: Path) -> dict[str, Any]:
    """Same path as `closed-sandbox diff`: written JSON in, diff dict out."""
    write_json(a, tmp_path / "a.json")
    write_json(b, tmp_path / "b.json")
    return diff_metrics(
        load_metrics_json(tmp_path / "a.json"),
        load_metrics_json(tmp_path / "b.json"),
    )


def _shape(md: str) -> list[str]:
    """Report structure only: headings, bullet labels, table column layout."""
    shape: list[str] = []
    in_code = False
    for line in md.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            shape.append("```")
        elif in_code:
            continue
        elif line.startswith("#"):
            shape.append(line)
        elif line.startswith("- "):
            shape.append(line.split(":", 1)[0] + ":")
        elif line.startswith("| scenario "):
            shape.append(line)
        elif line.startswith("|"):
            shape.append(f"|cols={line.count('|')}")
    return shape


# --- golden assertions ------------------------------------------------------


def test_report_md_is_byte_exact(tmp_path: Path) -> None:
    metrics = json.loads(FROZEN_A.read_text(encoding="utf-8"))
    assert _rendered(metrics, tmp_path) == REPORT_MD.read_text(encoding="utf-8")


def test_diff_output_is_byte_exact(tmp_path: Path) -> None:
    a = json.loads(FROZEN_A.read_text(encoding="utf-8"))
    b = json.loads(FROZEN_B.read_text(encoding="utf-8"))
    rendered = json.dumps(_cli_diff(a, b, tmp_path), indent=2, sort_keys=True) + "\n"
    assert rendered == DIFF_JSON.read_text(encoding="utf-8")


def test_live_run_keeps_golden_shape(tmp_path: Path) -> None:
    """A real anomaly_v0 run may move numbers, never the report format."""
    live = _rendered(_frozen_run(42), tmp_path)
    assert _shape(live) == _shape(REPORT_MD.read_text(encoding="utf-8"))


def test_live_run_keeps_golden_metric_keys() -> None:
    frozen = json.loads(FROZEN_A.read_text(encoding="utf-8"))
    assert set(_frozen_run(42)) == set(frozen)


def test_non_spiking_report_is_byte_exact(register_domain, tmp_path: Path) -> None:
    register_domain(fx.COST_PROBE)
    rendered = _rendered(_frozen_cost_probe(), tmp_path)
    assert rendered == GENERIC_MD.read_text(encoding="utf-8")


def test_non_spiking_report_has_no_spike_columns(
    register_domain, tmp_path: Path
) -> None:
    register_domain(fx.COST_PROBE)
    rendered = _rendered(_frozen_cost_probe(), tmp_path)
    table = rendered.split("## Per scenario", 1)[1].split("## Raw metrics", 1)[0]
    assert "spike_count" not in table
    assert "synops" not in table
    assert "n/a" not in table
    assert "quality_per_kspike" not in rendered
    assert "quality_per_unit_cost" in rendered


def _regenerate() -> None:
    sys.modules[f"closed_sandbox.domains.{fx.COST_DOMAIN_ID}"] = fx.COST_PROBE
    GOLDEN.mkdir(parents=True, exist_ok=True)
    tmp = GOLDEN / "_tmp"
    tmp.mkdir(exist_ok=True)

    a, b = _frozen_run(42), _frozen_run(43)
    for path, metrics in ((FROZEN_A, a), (FROZEN_B, b)):
        # Natural run order, not sorted: scenario rows must stay in manifest
        # order so the frozen input renders like a real run.
        path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    write_markdown(a, REPORT_MD)
    DIFF_JSON.write_text(
        json.dumps(_cli_diff(a, b, tmp), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(_frozen_cost_probe(), GENERIC_MD)

    for leftover in tmp.iterdir():
        leftover.unlink()
    tmp.rmdir()
    print(f"regenerated golden files in {GOLDEN}")


if __name__ == "__main__":
    _regenerate()
