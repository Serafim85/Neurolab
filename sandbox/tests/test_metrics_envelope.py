"""Common metrics envelope (NL-ADR-025): core minimum + SNN-family strictness."""

from __future__ import annotations

import copy
import importlib
import json
from pathlib import Path

import pytest

import fixture_domains as fx
from closed_sandbox.engine import EngineError, metrics_family, run_project
from closed_sandbox.manifest import ManifestError, load_project, validate_project
from closed_sandbox.report import enrich_economy, write_json

ROOT = Path(__file__).resolve().parents[1]

SNN_FAMILY_DOMAINS = ("snn_lif", "neuro_chip", "biosignal", "hybrid")
GENERIC_FAMILY_DOMAINS = ("biocompute", "synapse_import")


# --- family declarations ----------------------------------------------------


@pytest.mark.parametrize("domain_id", SNN_FAMILY_DOMAINS)
def test_shipped_snn_domains_declare_snn_family(domain_id: str) -> None:
    mod = importlib.import_module(f"closed_sandbox.domains.{domain_id}")
    assert metrics_family(mod) == "snn"


@pytest.mark.parametrize("domain_id", GENERIC_FAMILY_DOMAINS)
def test_non_spiking_domains_declare_generic_family(domain_id: str) -> None:
    mod = importlib.import_module(f"closed_sandbox.domains.{domain_id}")
    assert metrics_family(mod) == "generic"


def test_family_defaults_to_generic() -> None:
    assert metrics_family(fx.COST_PROBE) == "generic"


def test_unknown_family_is_rejected(register_domain) -> None:
    domain_id = register_domain(fx.BAD_FAMILY)
    with pytest.raises(EngineError, match="METRICS_FAMILY"):
        run_project(fx.minimal_project(domain_id))


# --- a domain with no spikes at all ----------------------------------------


def test_domain_without_spikes_runs(register_domain) -> None:
    register_domain(fx.COST_PROBE)
    metrics = run_project(copy.deepcopy(fx.COST_PROBE_PROJECT))

    assert "spike_count" not in metrics
    assert "synops" not in metrics
    assert "f1" not in metrics and "accuracy" not in metrics
    assert metrics["metric_primary"] == "fit_score"
    assert metrics["fit_score"] == 0.75
    assert metrics["budget_ok"] is True
    assert metrics["domain"] == fx.COST_DOMAIN_ID
    assert metrics["wall_ms"] >= 0.0


def test_stub_by_scenario_carries_primary_and_cost(register_domain) -> None:
    register_domain(fx.COST_PROBE)
    metrics = run_project(copy.deepcopy(fx.COST_PROBE_PROJECT))

    assert metrics["by_scenario_mode"] == "stub"
    assert set(metrics["by_scenario"]) == {"baseline", "stretch"}
    row = metrics["by_scenario"]["baseline"]
    assert row["fit_score"] == 0.75
    assert row["unit_cost_eur"] == 12.5
    assert "spike_count" not in row


# --- SNN family keeps the old strictness ------------------------------------


def test_snn_family_still_requires_spikes(register_domain) -> None:
    domain_id = register_domain(fx.BAD_SNN_SPIKES)
    with pytest.raises(EngineError, match="spike_count"):
        run_project(fx.minimal_project(domain_id))


def test_snn_family_still_requires_f1_or_accuracy(register_domain) -> None:
    domain_id = register_domain(fx.BAD_SNN_QUALITY)
    with pytest.raises(EngineError, match="f1' or 'accuracy"):
        run_project(fx.minimal_project(domain_id))


def test_synapse_import_keeps_source_strictness(tmp_path: Path) -> None:
    """Generic family, but the plugin still refuses an SNN export without cost keys."""
    from closed_sandbox.domains import synapse_import

    source = tmp_path / "src.json"
    source.write_text(json.dumps({"accuracy": 0.9, "synops": 10}), encoding="utf-8")
    with pytest.raises(ManifestError, match="spike_count"):
        synapse_import._load_source(source)


# --- core envelope errors ---------------------------------------------------


@pytest.mark.parametrize(
    "plugin,message",
    [
        (fx.BAD_NO_PRIMARY, "metric_primary"),
        (fx.BAD_PRIMARY_MISSING_VALUE, "returned no 'fit_score'"),
        (fx.BAD_PRIMARY_NOT_NUMBER, "must be a number"),
        (fx.BAD_NO_BUDGET_OK, "budget_ok"),
        (fx.BAD_BUDGET_OK_TYPE, "must be a bool"),
    ],
)
def test_envelope_violations_raise(register_domain, plugin, message: str) -> None:
    domain_id = register_domain(plugin)
    with pytest.raises(EngineError, match=message):
        run_project(fx.minimal_project(domain_id))


# --- [economy] cost_key -----------------------------------------------------


def test_generic_cost_key_proxy(register_domain) -> None:
    register_domain(fx.COST_PROBE)
    metrics = run_project(copy.deepcopy(fx.COST_PROBE_PROJECT))
    assert metrics["economy_cost_key"] == "unit_cost_eur"
    assert metrics["economy_cost_unit"] == "EUR"

    enriched = enrich_economy(metrics)
    assert enriched["quality_per_unit_cost"] == round(0.75 / 12.5, 6)
    assert "quality_per_kspike" not in enriched


def test_cost_key_absent_means_no_proxy(register_domain) -> None:
    register_domain(fx.COST_PROBE)
    project = copy.deepcopy(fx.COST_PROBE_PROJECT)
    project.pop("economy")
    metrics = run_project(project)
    assert "economy_cost_key" not in metrics
    assert "quality_per_unit_cost" not in enrich_economy(metrics)


def test_zero_cost_gets_no_ratio() -> None:
    """spike_count 0 (biocompute / synapse_import) must not fake a spike proxy."""
    enriched = enrich_economy(
        {
            "metric_primary": "accuracy",
            "accuracy": 0.86,
            "spike_count": 0,
            "synops": 0,
            "economy_cost_key": "spike_count",
        }
    )
    assert "quality_per_kspike" not in enriched
    assert "quality_per_ksynop" not in enriched
    assert "quality_per_unit_cost" not in enriched


def test_spike_proxies_unchanged_for_snn() -> None:
    enriched = enrich_economy(
        {"metric_primary": "f1", "f1": 0.9, "spike_count": 300, "synops": 1000}
    )
    assert enriched["quality_per_kspike"] == round(1000.0 * 0.9 / 300.0, 6)
    assert enriched["quality_per_ksynop"] == round(1000.0 * 0.9 / 1000.0, 6)


def test_chip_example_reports_unit_cost(tmp_path: Path) -> None:
    project = load_project(ROOT / "examples" / "chip_estimate_v0" / "project.toml")
    metrics = run_project(project, seed=42)
    write_json(metrics, tmp_path / "metrics.json")
    data = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))

    assert data["economy_cost_key"] == "chip_power_mw"
    assert data["quality_per_unit_cost"] == round(
        data["chip_fit_score"] / data["chip_power_mw"], 6
    )
    # Spike proxies survive alongside the generic one.
    assert "quality_per_kspike" in data


# --- manifest validation ----------------------------------------------------


def test_economy_defaults_to_empty_table() -> None:
    project = {"project": {"id": "x", "domain": "snn_lif"}}
    validate_project(project)
    assert project["economy"] == {}


@pytest.mark.parametrize("bad", [123, "", "   "])
def test_bad_cost_key_rejected(bad) -> None:
    project = {
        "project": {"id": "x", "domain": "snn_lif"},
        "economy": {"cost_key": bad},
    }
    with pytest.raises(ManifestError, match="cost_key"):
        validate_project(project)


def test_bad_cost_unit_rejected() -> None:
    project = {
        "project": {"id": "x", "domain": "snn_lif"},
        "economy": {"cost_key": "chip_power_mw", "cost_unit": 5},
    }
    with pytest.raises(ManifestError, match="cost_unit"):
        validate_project(project)
