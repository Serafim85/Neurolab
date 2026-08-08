"""Test-only domain plugins.

These never live in `closed_sandbox/domains/` — a new shipped domain needs an
ADR. They exist to prove the core metrics envelope (NL-ADR-025) works for a
domain that has no spikes at all, and that the SNN family stays strict.

Registration trick: `engine._load_plugin` resolves a domain through
`importlib.import_module("closed_sandbox.domains.<id>")`, which returns an
already-present `sys.modules` entry as-is. Tests insert these modules there via
the `register_domain` fixture in `conftest.py`.
"""

from __future__ import annotations

from types import ModuleType
from typing import Any, Callable

from closed_sandbox.manifest import ManifestError


def make_plugin(
    domain_id: str,
    *,
    run: Callable[..., dict[str, Any]],
    family: str | None = None,
    validate: Callable[[dict[str, Any]], None] | None = None,
) -> ModuleType:
    """Build a minimal domain plugin module honouring the plugin contract."""
    mod = ModuleType(f"closed_sandbox.domains.{domain_id}")
    mod.DOMAIN_ID = domain_id  # type: ignore[attr-defined]
    if family is not None:
        mod.METRICS_FAMILY = family  # type: ignore[attr-defined]
    mod.validate_project = validate or (lambda project: None)  # type: ignore[attr-defined]
    mod.run = run  # type: ignore[attr-defined]
    return mod


# --- D-none: a cost/budget estimator with no spikes and no f1 ---------------

COST_DOMAIN_ID = "cost_probe_test"


def _validate_cost_probe(project: dict[str, Any]) -> None:
    if "estimate" not in project:
        raise ManifestError("cost_probe_test requires [estimate]")
    if "max_unit_cost_eur" not in project.get("budget", {}):
        raise ManifestError("[budget] missing key: max_unit_cost_eur")


def _run_cost_probe(project: dict[str, Any], *, seed: int) -> dict[str, Any]:
    """Deterministic non-spiking domain: fit headroom under a money budget."""
    unit_cost = float(project["estimate"]["unit_cost_eur"])
    cap = float(project["budget"]["max_unit_cost_eur"])
    fit_score = round(max(0.0, 1.0 - unit_cost / cap), 4)
    return {
        "metric_primary": "fit_score",
        "fit_score": fit_score,
        "unit_cost_eur": unit_cost,
        "budget_ok": unit_cost <= cap,
        "latency_proxy_ms": 1.5,
        "n_test": 2,
        "estimate_disclaimer": "lab cost proxy — not a quote",
    }


COST_PROBE = make_plugin(
    COST_DOMAIN_ID, run=_run_cost_probe, validate=_validate_cost_probe
)

COST_PROBE_PROJECT: dict[str, Any] = {
    "project": {"id": "cost-probe", "domain": COST_DOMAIN_ID},
    "estimate": {"unit_cost_eur": 12.5},
    "budget": {"max_unit_cost_eur": 50.0},
    "sandbox": {"seed": 7, "scenarios": ["baseline", "stretch"]},
    "economy": {"cost_key": "unit_cost_eur", "cost_unit": "EUR"},
}


# --- broken plugins: each violates exactly one envelope rule ----------------

BAD_SNN_SPIKES = make_plugin(
    "bad_snn_spikes_test",
    family="snn",
    run=lambda project, *, seed: {
        "metric_primary": "f1",
        "f1": 0.9,
        "budget_ok": True,
    },
)

BAD_SNN_QUALITY = make_plugin(
    "bad_snn_quality_test",
    family="snn",
    run=lambda project, *, seed: {
        "metric_primary": "fit_score",
        "fit_score": 0.9,
        "spike_count": 10,
        "synops": 100,
        "budget_ok": True,
    },
)

BAD_NO_PRIMARY = make_plugin(
    "bad_no_primary_test",
    run=lambda project, *, seed: {"f1": 0.9, "budget_ok": True},
)

BAD_PRIMARY_NOT_NUMBER = make_plugin(
    "bad_primary_value_test",
    run=lambda project, *, seed: {
        "metric_primary": "verdict",
        "verdict": "looks fine",
        "budget_ok": True,
    },
)

BAD_PRIMARY_MISSING_VALUE = make_plugin(
    "bad_primary_missing_test",
    run=lambda project, *, seed: {"metric_primary": "fit_score", "budget_ok": True},
)

BAD_NO_BUDGET_OK = make_plugin(
    "bad_no_budget_ok_test",
    run=lambda project, *, seed: {"metric_primary": "f1", "f1": 0.9},
)

BAD_BUDGET_OK_TYPE = make_plugin(
    "bad_budget_ok_type_test",
    run=lambda project, *, seed: {
        "metric_primary": "f1",
        "f1": 0.9,
        "budget_ok": "yes",
    },
)

BAD_FAMILY = make_plugin(
    "bad_family_test",
    family="spiking-ish",
    run=lambda project, *, seed: {
        "metric_primary": "f1",
        "f1": 0.9,
        "budget_ok": True,
    },
)


def minimal_project(domain_id: str) -> dict[str, Any]:
    return {
        "project": {"id": f"{domain_id}-probe", "domain": domain_id},
        "sandbox": {"seed": 0, "scenarios": ["only"]},
    }
