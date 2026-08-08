"""Domain: import Synapse (or other lab) metrics into Closed Sandbox schema.

Does **not** run torch / Synapse runtime. Consumes a frozen JSON fixture or
export summary so sandbox `run` / `diff` / `ask` work on Synapse KPIs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from closed_sandbox.manifest import ManifestError

DOMAIN_ID = "synapse_import"

_REQUIRED_SOURCE = ("accuracy", "spike_count", "synops")


def validate_project(project: dict[str, Any]) -> None:
    if project["project"]["domain"] != DOMAIN_ID:
        raise ManifestError(
            f"domain mismatch: expected {DOMAIN_ID}, got {project['project']['domain']}"
        )
    if "import" not in project:
        raise ManifestError("synapse_import requires [import]")
    imp = project["import"]
    if "source" not in imp:
        raise ManifestError("[import].source path required (JSON metrics fixture)")
    if "budget" not in project:
        raise ManifestError("synapse_import requires [budget]")
    for key in ("max_neurons", "max_synapses", "max_spikes_per_sample"):
        if key not in project["budget"]:
            raise ManifestError(f"[budget] missing key: {key}")


def _resolve_source(project: dict[str, Any]) -> Path:
    raw = Path(project["import"]["source"])
    if raw.is_file():
        return raw.resolve()
    base = Path(project["_project_dir"])
    candidate = (base / raw).resolve()
    if candidate.is_file():
        return candidate
    raise ManifestError(f"[import].source not found: {raw}")


def _load_source(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ManifestError(f"import source must be a JSON object: {path}")
    for key in _REQUIRED_SOURCE:
        if key not in data:
            raise ManifestError(f"import source missing key '{key}': {path}")
    return data


def run(project: dict[str, Any], *, seed: int) -> dict[str, Any]:
    path = _resolve_source(project)
    src = _load_source(path)
    budget = project["budget"]

    n_neurons = int(src.get("n_neurons", project.get("network", {}).get("n_neurons", 0)))
    n_synapses = int(
        src.get("n_synapses", project.get("network", {}).get("n_synapses", 0))
    )
    spike_count = int(src["spike_count"])
    synops = int(src["synops"])
    max_spikes = int(budget["max_spikes_per_sample"])

    budget_ok = (
        n_neurons <= int(budget["max_neurons"])
        and n_synapses <= int(budget["max_synapses"])
        and spike_count <= max_spikes
        and bool(src.get("budget_ok", True))
    )

    accuracy = float(src["accuracy"])
    # Prefer explicit f1; else mirror accuracy for schema compatibility.
    f1 = float(src["f1"]) if "f1" in src else accuracy

    metrics: dict[str, Any] = {
        "accuracy": round(accuracy, 4),
        "f1": round(f1, 4),
        "spike_count": spike_count,
        "synops": synops,
        "latency_proxy_ms": float(src.get("latency_proxy_ms", src.get("latency_ms", 0.0))),
        "budget_ok": budget_ok,
        "n_neurons": n_neurons,
        "n_synapses": n_synapses,
        "metric_primary": project.get("task", {}).get("metric_primary", "accuracy"),
        "import_source": str(path),
        "synapse_pack": src.get("pack", project["import"].get("pack", "")),
        "escalate_rate": src.get("escalate_rate"),
        "oracle_accuracy": src.get("oracle_accuracy"),
        "class_fix": src.get("class_fix"),
        "brain_role": src.get("brain_role"),
        "stub_accuracy": src.get("stub_accuracy"),
        "stage_vote_accuracy": src.get("stage_vote_accuracy"),
        "specialist_accuracy": src.get("specialist_accuracy"),
        "rescue_accuracy": src.get("rescue_accuracy"),
        "bridge_version": src.get("bridge_version"),
        "notes": src.get("notes", ""),
        "seed": seed,
    }
    # Drop Nones for clean JSON
    return {k: v for k, v in metrics.items() if v is not None}
