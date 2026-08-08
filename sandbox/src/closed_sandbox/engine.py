"""Dispatch runs to domain plugins."""

from __future__ import annotations

import importlib
import time
from typing import Any, Protocol


from closed_sandbox.report import ensure_by_scenario


class DomainPlugin(Protocol):
    DOMAIN_ID: str

    def validate_project(self, project: dict[str, Any]) -> None: ...

    def run(self, project: dict[str, Any], *, seed: int) -> dict[str, Any]: ...


class EngineError(RuntimeError):
    """Domain dispatch or run failure."""


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

    required = ("spike_count", "synops", "budget_ok")
    for key in required:
        if key not in metrics:
            raise EngineError(f"domain '{domain_id}' metrics missing key: {key}")
    if "f1" not in metrics and "accuracy" not in metrics:
        raise EngineError(
            f"domain '{domain_id}' metrics must include 'f1' or 'accuracy'"
        )
    if "latency_proxy_ms" not in metrics:
        metrics["latency_proxy_ms"] = round(elapsed_ms, 3)
    # Always record wall clock (domain may set sim-step latency_proxy separately).
    metrics["wall_ms"] = round(elapsed_ms, 3)

    metrics.setdefault("domain", domain_id)
    metrics.setdefault("seed", run_seed)
    metrics.setdefault("project_id", project["project"]["id"])
    ensure_by_scenario(metrics, project)
    if isinstance(metrics.get("by_scenario"), dict) and "by_scenario_mode" not in metrics:
        # Plugin-supplied split (D0–D4 generative conditions).
        metrics["by_scenario_mode"] = "split"
    return metrics
