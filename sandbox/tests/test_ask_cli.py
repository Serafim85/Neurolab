"""CLI ask against live Outpost (integration)."""

from __future__ import annotations

from pathlib import Path

import pytest

from closed_sandbox.cli import main
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import load_project
from closed_sandbox.report import write_json

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "anomaly_v0" / "project.toml"


def test_cli_ask_mentions_budget(outpost_base_url: str, tmp_path: Path, capsys) -> None:
    project = load_project(EXAMPLE)
    project["contour"]["provider"] = "local"
    project["contour"]["base_url"] = outpost_base_url
    project["contour"]["model"] = "outpost-tiny-hammer"
    metrics = run_project(project, seed=42)
    metrics_path = tmp_path / "metrics.json"
    write_json(metrics, metrics_path)

    # Overlay contour into a temp project.toml copy for CLI
    import tomllib

    raw = EXAMPLE.read_bytes()
    data = tomllib.loads(raw.decode("utf-8"))
    data["contour"]["provider"] = "local"
    data["contour"]["base_url"] = outpost_base_url
    data["contour"]["model"] = "outpost-tiny-hammer"

    # Write minimal TOML by hand (stdlib has no tomli_w)
    proj_path = tmp_path / "project.toml"
    proj_path.write_text(
        "\n".join(
            [
                "[project]",
                f'id = "{data["project"]["id"]}"',
                f'name = "{data["project"]["name"]}"',
                f'version = "{data["project"]["version"]}"',
                f'domain = "{data["project"]["domain"]}"',
                "",
                "[network]",
                f'kind = "{data["network"]["kind"]}"',
                f'n_inputs = {data["network"]["n_inputs"]}',
                f'n_hidden = {data["network"]["n_hidden"]}',
                f'n_outputs = {data["network"]["n_outputs"]}',
                'neuron = "lif"',
                f'dt_ms = {data["network"]["dt_ms"]}',
                f'sim_steps = {data["network"].get("sim_steps", 24)}',
                "",
                "[budget]",
                f'max_neurons = {data["budget"]["max_neurons"]}',
                f'max_synapses = {data["budget"]["max_synapses"]}',
                f'max_spikes_per_sample = {data["budget"]["max_spikes_per_sample"]}',
                "",
                "[task]",
                'kind = "binary_anomaly"',
                'dataset = "data"',
                'metric_primary = "f1"',
                "",
                "[sandbox]",
                "seed = 42",
                "",
                "[contour]",
                "ask_enabled = true",
                'provider = "local"',
                f'base_url = "{outpost_base_url}"',
                'model = "outpost-tiny-hammer"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    try:
        main(
            [
                "ask",
                str(proj_path),
                "State whether budget_ok is true. One short sentence.",
                "--metrics",
                str(metrics_path),
            ]
        )
    except SystemExit as exc:
        assert exc.code == 0, exc.code

    out = capsys.readouterr().out.lower()
    assert "budget" in out
    assert len(out.strip()) >= 10
