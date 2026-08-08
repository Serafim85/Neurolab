"""Domain D1: neuromorphic chip rough map / estimate (not PDK / not tape-out).

Maps SNN topology (+ optional prior run metrics) to proxy chip_* metrics
for a named target profile. Numbers are **lab estimates**, not silicon truth.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from closed_sandbox.manifest import ManifestError

DOMAIN_ID = "neuro_chip"

# Named targets — order-of-magnitude lab proxies only (NL-ADR-020/021).
# Not vendor datasheets; not bitstream / SDK builds.
_TARGETS: dict[str, dict[str, Any]] = {
    "generic_neuromorphic_v0": {
        "class": "asic_style_proxy",
        "area_um2_per_neuron": 25.0,
        "area_um2_per_synapse": 2.5,
        "energy_pj_per_synop": 0.5,
        "energy_pj_per_spike": 2.0,
        "latency_ns_per_synop": 0.05,
        "latency_base_us": 10.0,
        "assumed_samples_per_s": 100.0,
    },
    # Mid-range FPGA fabric proxy for a compact LIF SNN (LUT/BRAM/DSP heuristics).
    # "area_mm2" here ≈ package/board footprint proxy, not a die size claim.
    "fpga_snn_lite_v0": {
        "class": "fpga",
        "area_um2_per_neuron": 1200.0,
        "area_um2_per_synapse": 80.0,
        "energy_pj_per_synop": 8.0,
        "energy_pj_per_spike": 25.0,
        "latency_ns_per_synop": 2.0,
        "latency_base_us": 50.0,
        "assumed_samples_per_s": 100.0,
        "luts_per_neuron": 48.0,
        "luts_per_synapse": 3.0,
        "bram18_per_1k_synapses": 1.25,
        "dsp_per_output": 2.0,
        "export_schema": "fpga_snn_lite_v0.export.v1",
    },
}


def list_targets() -> list[str]:
    return sorted(_TARGETS)


def validate_project(project: dict[str, Any]) -> None:
    if project["project"]["domain"] != DOMAIN_ID:
        raise ManifestError(
            f"domain mismatch: expected {DOMAIN_ID}, got {project['project']['domain']}"
        )
    if "network" not in project:
        raise ManifestError("neuro_chip requires [network]")
    net = project["network"]
    for key in ("n_inputs", "n_hidden", "n_outputs"):
        if key not in net:
            raise ManifestError(f"[network] missing key: {key}")
    if "chip" not in project:
        raise ManifestError("neuro_chip requires [chip]")
    chip = project["chip"]
    target = chip.get("target")
    if not target or target not in _TARGETS:
        raise ManifestError(
            f"[chip].target must be one of {list_targets()}; got {target!r}"
        )
    if "budget" not in project:
        raise ManifestError("neuro_chip requires [budget]")
    for key in ("max_neurons", "max_synapses", "max_spikes_per_sample"):
        if key not in project["budget"]:
            raise ManifestError(f"[budget] missing key: {key}")
    for key in ("max_chip_power_mw", "max_chip_area_mm2"):
        if key not in project["budget"]:
            raise ManifestError(f"[budget] missing key: {key}")


def _topology(project: dict[str, Any]) -> tuple[int, int, int, int, int]:
    net = project["network"]
    n_in = int(net["n_inputs"])
    n_hid = int(net["n_hidden"])
    n_out = int(net["n_outputs"])
    n_neurons = n_hid + n_out  # inputs often pads / not counted as cores
    n_synapses = n_in * n_hid + n_hid * n_out
    return n_neurons, n_synapses, n_in, n_hid, n_out


def _load_source_metrics(project: dict[str, Any]) -> dict[str, Any] | None:
    raw = project.get("chip", {}).get("source_metrics")
    if not raw:
        return None
    path = Path(raw)
    if not path.is_file():
        path = Path(project["_project_dir"]) / raw
    if not path.is_file():
        raise ManifestError(f"[chip].source_metrics not found: {raw}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ManifestError("source_metrics must be a JSON object")
    return data


def _fpga_resources(
    coeffs: dict[str, Any], *, n_neurons: int, n_synapses: int, n_out: int
) -> dict[str, Any]:
    luts = int(
        round(n_neurons * float(coeffs["luts_per_neuron"]) + n_synapses * float(coeffs["luts_per_synapse"]))
    )
    bram18 = int(round((n_synapses / 1000.0) * float(coeffs["bram18_per_1k_synapses"])))
    dsp = int(round(n_out * float(coeffs["dsp_per_output"])))
    return {
        "chip_luts_est": max(1, luts),
        "chip_bram18_est": max(0, bram18),
        "chip_dsp_est": max(0, dsp),
    }


# Activity-load conditions (generative scenarios for chip estimate).
# Scales spike/synop activity from the baseline source; area stays topology-fixed.
_ACTIVITY: dict[str, tuple[float, float]] = {
    "nominal": (1.0, 1.0),
    "estimate": (1.0, 1.0),  # legacy single-name alias
    "high_activity": (1.85, 1.65),
    "sparse": (0.42, 0.48),
}
KNOWN_SCENARIOS = ("nominal", "high_activity", "sparse")


def _activity_scales(scenario: str) -> tuple[float, float]:
    return _ACTIVITY.get(scenario, _ACTIVITY["nominal"])


def _estimate_row(
    *,
    coeffs: dict[str, Any],
    budget: dict[str, Any],
    n_neurons: int,
    n_synapses: int,
    spike_count: int,
    synops: int,
    f1: float,
    accuracy: float,
) -> dict[str, Any]:
    area_um2 = (
        n_neurons * float(coeffs["area_um2_per_neuron"])
        + n_synapses * float(coeffs["area_um2_per_synapse"])
    )
    chip_area_mm2 = round(area_um2 / 1e6, 6)

    samples_per_s = float(coeffs["assumed_samples_per_s"])
    energy_pj = (
        synops * float(coeffs["energy_pj_per_synop"])
        + spike_count * float(coeffs["energy_pj_per_spike"])
    )
    chip_power_mw = round((energy_pj * 1e-9) * samples_per_s * 1e3, 6)

    latency_us = float(coeffs["latency_base_us"]) + synops * float(
        coeffs["latency_ns_per_synop"]
    ) * 1e-3
    latency_proxy_ms = round(latency_us / 1000.0, 6)

    budget_ok = (
        n_neurons <= int(budget["max_neurons"])
        and n_synapses <= int(budget["max_synapses"])
        and spike_count <= int(budget["max_spikes_per_sample"])
        and chip_power_mw <= float(budget["max_chip_power_mw"])
        and chip_area_mm2 <= float(budget["max_chip_area_mm2"])
    )

    power_head = 1.0 - (chip_power_mw / float(budget["max_chip_power_mw"]))
    area_head = 1.0 - (chip_area_mm2 / float(budget["max_chip_area_mm2"]))
    chip_fit_score = round(max(0.0, min(1.0, min(power_head, area_head))), 4)

    return {
        "n": 1,
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "spike_count": spike_count,
        "synops": synops,
        "latency_proxy_ms": latency_proxy_ms,
        "budget_ok": budget_ok,
        "chip_area_mm2": chip_area_mm2,
        "chip_power_mw": chip_power_mw,
        "chip_energy_pj_per_sample": round(energy_pj, 3),
        "chip_fit_score": chip_fit_score,
    }


def run(project: dict[str, Any], *, seed: int) -> dict[str, Any]:
    chip = project["chip"]
    target = str(chip["target"])
    coeffs = _TARGETS[target]
    n_neurons, n_synapses, n_in, n_hid, n_out = _topology(project)
    src = _load_source_metrics(project)

    if src is not None:
        base_spikes = int(src.get("spike_count", max(1, n_neurons // 2)))
        base_synops = int(src.get("synops", n_synapses))
        f1 = float(src["f1"]) if "f1" in src else None
        accuracy = float(src["accuracy"]) if "accuracy" in src else None
        if f1 is None and accuracy is not None:
            f1 = accuracy
        if accuracy is None and f1 is not None:
            accuracy = f1
        if f1 is None:
            f1 = 0.0
            accuracy = 0.0
        source_note = "from_source_metrics"
    else:
        base_spikes = max(1, int(n_neurons * 5))
        base_synops = max(1, int(n_synapses * 0.35))
        f1 = 0.0
        accuracy = 0.0
        source_note = "topology_heuristic"

    budget = project["budget"]
    scenario_names = list(project.get("sandbox", {}).get("scenarios") or [])
    if not scenario_names:
        scenario_names = list(KNOWN_SCENARIOS)

    by_scenario: dict[str, Any] = {}
    for name in scenario_names:
        spike_s, synop_s = _activity_scales(name)
        spikes = max(1, int(round(base_spikes * spike_s)))
        synops = max(1, int(round(base_synops * synop_s)))
        by_scenario[name] = _estimate_row(
            coeffs=coeffs,
            budget=budget,
            n_neurons=n_neurons,
            n_synapses=n_synapses,
            spike_count=spikes,
            synops=synops,
            f1=f1,
            accuracy=accuracy,
        )

    # Aggregate = first scenario (manifest order) — usually "nominal".
    primary_row = by_scenario[scenario_names[0]]
    primary = project.get("task", {}).get("metric_primary", "chip_fit_score")
    chip_class = str(coeffs.get("class", "unknown"))

    disclaimer = (
        "lab proxy coefficients — not silicon / not PDK / not bitstream; "
        "do not cite as measured Joules or vendor utilization"
    )

    metrics: dict[str, Any] = {
        "f1": primary_row["f1"],
        "accuracy": primary_row["accuracy"],
        "spike_count": primary_row["spike_count"],
        "synops": primary_row["synops"],
        "latency_proxy_ms": primary_row["latency_proxy_ms"],
        "budget_ok": primary_row["budget_ok"],
        "n_neurons": n_neurons,
        "n_synapses": n_synapses,
        "n_test": len(scenario_names),
        "metric_primary": primary,
        "chip_target": target,
        "chip_class": chip_class,
        "chip_area_mm2": primary_row["chip_area_mm2"],
        "chip_power_mw": primary_row["chip_power_mw"],
        "chip_energy_pj_per_sample": primary_row["chip_energy_pj_per_sample"],
        "chip_fit_score": primary_row["chip_fit_score"],
        "chip_estimate_kind": source_note,
        "chip_estimate_disclaimer": disclaimer,
        "seed": seed,
        "by_scenario": by_scenario,
        "by_scenario_mode": "split",
    }

    if chip_class == "fpga":
        resources = _fpga_resources(
            coeffs, n_neurons=n_neurons, n_synapses=n_synapses, n_out=n_out
        )
        metrics.update(resources)
        if "max_chip_luts" in budget:
            lut_ok = resources["chip_luts_est"] <= int(budget["max_chip_luts"])
            metrics["budget_ok"] = metrics["budget_ok"] and lut_ok
            for row in by_scenario.values():
                row["budget_ok"] = bool(row["budget_ok"] and lut_ok)
        export = {
            "schema": coeffs.get("export_schema", "fpga_export.v0"),
            "target": target,
            "chip_class": chip_class,
            "network": {
                "n_inputs": n_in,
                "n_hidden": n_hid,
                "n_outputs": n_out,
                "n_neurons": n_neurons,
                "n_synapses": n_synapses,
            },
            "activity": {
                "spike_count": primary_row["spike_count"],
                "synops": primary_row["synops"],
                "seed": seed,
                "by_scenario": {
                    k: {"spike_count": v["spike_count"], "synops": v["synops"]}
                    for k, v in by_scenario.items()
                },
            },
            "resource_proxy": {
                "luts_est": resources["chip_luts_est"],
                "bram18_est": resources["chip_bram18_est"],
                "dsp_est": resources["chip_dsp_est"],
                "power_mw_est": primary_row["chip_power_mw"],
                "area_mm2_est": primary_row["chip_area_mm2"],
                "latency_proxy_ms": primary_row["latency_proxy_ms"],
            },
            "fit": {
                "chip_fit_score": primary_row["chip_fit_score"],
                "budget_ok": metrics["budget_ok"],
            },
            "disclaimer": disclaimer,
            "next_hooks": [
                "map resource_proxy to vendor utilization report (human)",
                "no automatic Vivado/Quartus/bitstream in sandbox v0",
            ],
        }
        metrics["chip_export"] = export

    return metrics
