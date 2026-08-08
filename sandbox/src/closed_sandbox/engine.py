"""Dispatch runs to domain plugins and enforce the common metrics envelope.

Envelope (NL-ADR-025): every domain owes `metric_primary`, a numeric value under
that name, and `budget_ok`. A plugin that declares `METRICS_FAMILY = "snn"`
additionally owes `spike_count` / `synops` / (`f1` or `accuracy`).
"""

from __future__ import annotations

import importlib
import time
from typing import Any, Protocol


from closed_sandbox.report import ensure_by_scenario


#: Metrics families a plugin may declare via module-level ``METRICS_FAMILY``.
#: ``generic`` (default) only owes the core envelope; ``snn`` additionally owes
#: the spiking cost keys that D0/D1/D3/D4 have always reported.
METRICS_FAMILIES = ("generic", "snn")
DEFAULT_METRICS_FAMILY = "generic"

#: Core envelope every domain must return (NL-ADR-025).
CORE_REQUIRED_KEYS = ("metric_primary", "budget_ok")
#: Extra keys required from the SNN family.
SNN_REQUIRED_KEYS = ("spike_count", "synops")


class DomainPlugin(Protocol):
    DOMAIN_ID: str

    def validate_project(self, project: dict[str, Any]) -> None: ...

    def run(self, project: dict[str, Any], *, seed: int) -> dict[str, Any]: ...


class EngineError(RuntimeError):
    """Domain dispatch or run failure."""


def metrics_family(plugin: Any) -> str:
    """Declared metrics family of a plugin (``generic`` when unset)."""
    family = getattr(plugin, "METRICS_FAMILY", DEFAULT_METRICS_FAMILY)
    if family not in METRICS_FAMILIES:
        raise EngineError(
            f"domain plugin '{getattr(plugin, 'DOMAIN_ID', '?')}' declares "
            f"METRICS_FAMILY={family!r}; use one of {METRICS_FAMILIES}"
        )
    return str(family)


def _as_number(value: Any) -> float | int | None:
    """Python number from a metric value, or None if it is not numeric."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    # numpy scalars: keep JSON serializable without importing numpy here.
    item = getattr(value, "item", None)
    if callable(item):
        inner = item()
        if isinstance(inner, (int, float)) and not isinstance(inner, bool):
            return inner
    return None


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    item = getattr(value, "item", None)
    if callable(item):
        inner = item()
        if isinstance(inner, bool):
            return inner
    return None


def _check_envelope(
    metrics: dict[str, Any], *, domain_id: str, family: str
) -> None:
    """Enforce the common metrics envelope; normalize numpy scalars in place."""
    for key in CORE_REQUIRED_KEYS:
        if key not in metrics:
            raise EngineError(f"domain '{domain_id}' metrics missing key: {key}")

    primary = metrics["metric_primary"]
    if not isinstance(primary, str) or not primary:
        raise EngineError(
            f"domain '{domain_id}' metric_primary must be a non-empty string "
            f"naming the primary metric (e.g. 'f1'), got {primary!r}"
        )
    if primary not in metrics:
        raise EngineError(
            f"domain '{domain_id}' declares metric_primary={primary!r} "
            f"but returned no '{primary}' value"
        )
    value = _as_number(metrics[primary])
    if value is None:
        raise EngineError(
            f"domain '{domain_id}' metric '{primary}' must be a number, "
            f"got {metrics[primary]!r}"
        )
    metrics[primary] = value

    budget_ok = _as_bool(metrics["budget_ok"])
    if budget_ok is None:
        raise EngineError(
            f"domain '{domain_id}' metric 'budget_ok' must be a bool, "
            f"got {metrics['budget_ok']!r}"
        )
    metrics["budget_ok"] = budget_ok

    if family != "snn":
        return
    for key in SNN_REQUIRED_KEYS:
        if key not in metrics:
            raise EngineError(
                f"domain '{domain_id}' (METRICS_FAMILY=snn) metrics missing key: {key}"
            )
    if "f1" not in metrics and "accuracy" not in metrics:
        raise EngineError(
            f"domain '{domain_id}' (METRICS_FAMILY=snn) metrics must include "
            "'f1' or 'accuracy'"
        )


def _attach_economy(metrics: dict[str, Any], project: dict[str, Any]) -> None:
    """Carry `[economy]` from the manifest into metrics for report/diff."""
    economy = project.get("economy") or {}
    cost_key = economy.get("cost_key")
    if isinstance(cost_key, str) and cost_key.strip():
        metrics.setdefault("economy_cost_key", cost_key.strip())
    cost_unit = economy.get("cost_unit")
    if isinstance(cost_unit, str) and cost_unit.strip():
        metrics.setdefault("economy_cost_unit", cost_unit.strip())


def _load_plugin(domain_id: str) -> DomainPlugin:
    module_name = f"closed_sandbox.domains.{domain_id}"
    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise EngineError(
            f"unknown domain '{domain_id}'. "
            f"Implement closed_sandbox.domains.{domain_id} or fix [project].domain"
        ) from exc

    for attr in ("DOMAIN_ID", "validate_project", "run"):
        if not hasattr(mod, attr):
            raise EngineError(
                f"domain plugin '{domain_id}' missing required export: {attr}"
            )
    if mod.DOMAIN_ID != domain_id:
        raise EngineError(
            f"plugin DOMAIN_ID={mod.DOMAIN_ID!r} does not match domain {domain_id!r}"
        )
    metrics_family(mod)  # fail fast on a typo in METRICS_FAMILY
    return mod  # type: ignore[return-value]


def validate_loaded_project(project: dict[str, Any]) -> None:
    """Common + domain plugin validation (CLI/UI validate before run)."""
    from closed_sandbox.manifest import validate_project

    validate_project(project)
    domain_id = project["project"]["domain"]
    plugin = _load_plugin(domain_id)
    plugin.validate_project(project)


def run_project(project: dict[str, Any], *, seed: int | None = None) -> dict[str, Any]:
    """Validate, run domain plugin, attach wall-clock latency if missing."""
    domain_id = project["project"]["domain"]
    plugin = _load_plugin(domain_id)
    plugin.validate_project(project)

    run_seed = int(project["sandbox"]["seed"] if seed is None else seed)
    t0 = time.perf_counter()
    metrics = plugin.run(project, seed=run_seed)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    _check_envelope(metrics, domain_id=domain_id, family=metrics_family(plugin))
    if "latency_proxy_ms" not in metrics:
        metrics["latency_proxy_ms"] = round(elapsed_ms, 3)
    # Always record wall clock (domain may set sim-step latency_proxy separately).
    metrics["wall_ms"] = round(elapsed_ms, 3)

    metrics.setdefault("domain", domain_id)
    metrics.setdefault("seed", run_seed)
    metrics.setdefault("project_id", project["project"]["id"])
    _attach_economy(metrics, project)
    ensure_by_scenario(metrics, project)
    if isinstance(metrics.get("by_scenario"), dict) and "by_scenario_mode" not in metrics:
        # Plugin-supplied split (D0–D4 generative conditions).
        metrics["by_scenario_mode"] = "split"
    return metrics
