"""Domain D0: snn_lif — compact LIF SNN for binary anomaly on synthetic 1D signals."""

from __future__ import annotations

import random
from typing import Any

from closed_sandbox.domains.snn_lif.data import Sample, make_dataset
from closed_sandbox.domains.snn_lif.lif import LIFLayer, LIFParams, _HAS_NUMPY, count_synops
from closed_sandbox.manifest import ManifestError

if _HAS_NUMPY:
    import numpy as np

DOMAIN_ID = "snn_lif"
METRICS_FAMILY = "snn"


def validate_project(project: dict[str, Any]) -> None:
    if project["project"]["domain"] != DOMAIN_ID:
        raise ManifestError(
            f"domain mismatch: expected {DOMAIN_ID}, got {project['project']['domain']}"
        )
    if "network" not in project:
        raise ManifestError("snn_lif requires [network]")
    net = project["network"]
    for key in ("n_inputs", "n_hidden", "n_outputs", "kind"):
        if key not in net:
            raise ManifestError(f"[network] missing key: {key}")
    if net["kind"] != "snn_lif":
        raise ManifestError(f"[network].kind must be snn_lif, got {net['kind']!r}")
    if int(net["n_outputs"]) < 2:
        raise ManifestError("[network].n_outputs must be >= 2 for binary anomaly")

    if "budget" not in project:
        raise ManifestError("snn_lif requires [budget]")
    budget = project["budget"]
    for key in ("max_neurons", "max_synapses", "max_spikes_per_sample"):
        if key not in budget:
            raise ManifestError(f"[budget] missing key: {key}")

    if "task" not in project:
        raise ManifestError("snn_lif requires [task]")
    if project["task"].get("kind") != "binary_anomaly":
        raise ManifestError("[task].kind must be binary_anomaly in v0")


def _normalize(features: list[float]) -> list[float]:
    peak = max(abs(x) for x in features) or 1.0
    return [x / peak for x in features]


def _normalize_np(features: list[float]) -> "np.ndarray":
    arr = np.asarray(features, dtype=np.float64)
    peak = float(np.max(np.abs(arr))) or 1.0
    return arr / peak


def _forward(
    sample: Sample,
    hidden: LIFLayer,
    readout: LIFLayer,
    *,
    steps: int,
    account: bool = True,
) -> tuple[list[int], list[int], int, int]:
    """Run sample; return (hidden_counts, out_counts, spike_count, synops)."""
    hidden.reset()
    readout.reset()
    if _HAS_NUMPY and hidden._use_np:
        currents = _normalize_np(sample.features)
        h_counts = np.zeros(hidden.n_out, dtype=np.int64)
        o_counts = np.zeros(readout.n_out, dtype=np.int64)
        spikes_total = 0
        synops = 0
        for _ in range(steps):
            h_spikes = hidden.step_np(currents)
            h_counts += h_spikes
            if account:
                hs = int(h_spikes.sum())
                spikes_total += hs
                synops += hidden.n_in * hs
            o_spikes = readout.step_np(h_spikes.astype(np.float64))
            o_counts += o_spikes
            if account:
                os_ = int(o_spikes.sum())
                spikes_total += os_
                synops += readout.n_in * os_
        return h_counts.tolist(), o_counts.tolist(), spikes_total, synops

    currents = _normalize(sample.features)
    h_counts = [0] * hidden.n_out
    o_counts = [0] * readout.n_out
    spikes_total = 0
    synops = 0
    for _ in range(steps):
        h_spikes = hidden.step(currents)
        for i, s in enumerate(h_spikes):
            h_counts[i] += s
        if account:
            spikes_total += sum(h_spikes)
            synops += count_synops(hidden.n_in, h_spikes)
        o_spikes = readout.step([float(s) for s in h_spikes])
        for i, s in enumerate(o_spikes):
            o_counts[i] += s
        if account:
            spikes_total += sum(o_spikes)
            synops += count_synops(readout.n_in, o_spikes)
    return h_counts, o_counts, spikes_total, synops


def _predict_label(out_counts: list[int]) -> int:
    return 1 if out_counts[1] >= out_counts[0] else 0


def _f1_binary(y_true: list[int], y_pred: list[int]) -> float:
    tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == 1 and p == 0)
    if tp == 0:
        return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _bucket_metrics(
    y_true: list[int],
    y_pred: list[int],
    spikes: list[int],
    synops: list[int],
) -> dict[str, Any]:
    n = len(y_true)
    if n == 0:
        return {
            "n": 0,
            "f1": 0.0,
            "accuracy": 0.0,
            "spike_count": 0,
            "synops": 0,
        }
    accuracy = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == p) / n
    return {
        "n": n,
        "f1": round(_f1_binary(y_true, y_pred), 4),
        "accuracy": round(accuracy, 4),
        "spike_count": int(round(sum(spikes) / n)),
        "synops": int(round(sum(synops) / n)),
    }


def _train(
    train: list[Sample],
    hidden: LIFLayer,
    readout: LIFLayer,
    *,
    steps: int,
    seed: int,
    epochs: int = 20,
    lr: float = 0.1,
    early_acc: float = 0.98,
) -> int:
    """Perceptron-style updates; returns epochs actually run."""
    rng = random.Random(seed + 17)
    order = list(train)
    ran = 0
    for ep in range(epochs):
        rng.shuffle(order)
        step_lr = lr * (0.92**ep)
        correct = 0
        for sample in order:
            h_counts, o_counts, _, _ = _forward(
                sample, hidden, readout, steps=steps, account=False
            )
            pred = _predict_label(o_counts)
            target = sample.label
            if pred == target:
                correct += 1
                continue
            if hidden._use_np:
                for k, hk in enumerate(h_counts):
                    readout.weights_np[target, k] += step_lr * float(hk)
                    readout.weights_np[pred, k] -= step_lr * float(hk)
                mid = sample.features[
                    len(sample.features) // 3 : 2 * len(sample.features) // 3
                ]
                energy = sum(abs(x) for x in mid) / max(len(mid), 1)
                if sample.label == 1 and energy > 0.5:
                    feat = np.asarray(sample.features, dtype=np.float64)
                    hidden.weights_np[:8, :] += 0.003 * feat
                readout.weights = readout.weights_np.tolist()
                hidden.weights = hidden.weights_np.tolist()
            else:
                for k, hk in enumerate(h_counts):
                    readout.weights[target][k] += step_lr * float(hk)
                    readout.weights[pred][k] -= step_lr * float(hk)
                mid = sample.features[
                    len(sample.features) // 3 : 2 * len(sample.features) // 3
                ]
                energy = sum(abs(x) for x in mid) / max(len(mid), 1)
                if sample.label == 1 and energy > 0.5:
                    for j in range(min(8, hidden.n_out)):
                        for k in range(hidden.n_in):
                            hidden.weights[j][k] += 0.003 * sample.features[k]
        ran = ep + 1
        if correct / max(len(order), 1) >= early_acc:
            break
    return ran


def run(project: dict[str, Any], *, seed: int) -> dict[str, Any]:
    net = project["network"]
    budget = project["budget"]
    n_in = int(net["n_inputs"])
    n_hidden = int(net["n_hidden"])
    n_out = int(net["n_outputs"])
    dt_ms = float(net.get("dt_ms", 1.0))
    steps = int(net.get("sim_steps", 24))
    train_epochs = int(net.get("train_epochs", 20))

    n_neurons = n_hidden + n_out
    n_synapses = n_in * n_hidden + n_hidden * n_out
    max_spikes = int(budget["max_spikes_per_sample"])

    scenario_names = list(project.get("sandbox", {}).get("scenarios") or [])
    train, test = make_dataset(
        seed=seed,
        n_features=n_in,
        scenarios=scenario_names or None,
        n_train=120,
        n_test_per_scenario=14,
    )
    params = LIFParams(dt=dt_ms, tau=8.0, v_th=0.8)
    hidden = LIFLayer(n_in, n_hidden, seed=seed, params=params, weight_scale=0.45)
    readout = LIFLayer(
        n_hidden, n_out, seed=seed + 1, params=params, weight_scale=0.55
    )
    epochs_ran = _train(
        train,
        hidden,
        readout,
        steps=steps,
        seed=seed,
        epochs=train_epochs,
    )

    y_true: list[int] = []
    y_pred: list[int] = []
    spike_sum = 0
    synops_sum = 0
    over_budget = 0
    # scenario -> lists for per-scenario metrics
    buckets: dict[str, dict[str, list[int]]] = {}

    for sample in test:
        _, o_counts, spikes, synops = _forward(sample, hidden, readout, steps=steps)
        pred = _predict_label(o_counts)
        y_true.append(sample.label)
        y_pred.append(pred)
        spike_sum += spikes
        synops_sum += synops
        if spikes > max_spikes:
            over_budget += 1
        bucket = buckets.setdefault(
            sample.scenario, {"y_true": [], "y_pred": [], "spikes": [], "synops": []}
        )
        bucket["y_true"].append(sample.label)
        bucket["y_pred"].append(pred)
        bucket["spikes"].append(spikes)
        bucket["synops"].append(synops)

    f1 = _f1_binary(y_true, y_pred)
    accuracy = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == p) / len(
        y_true
    )
    avg_spikes = spike_sum / len(test)
    avg_synops = synops_sum / len(test)

    by_scenario = {
        name: _bucket_metrics(
            data["y_true"], data["y_pred"], data["spikes"], data["synops"]
        )
        for name, data in buckets.items()
    }
    # Stable order from manifest when present.
    ordered: dict[str, Any] = {}
    for name in scenario_names:
        if name in by_scenario:
            ordered[name] = by_scenario[name]
    for name, row in by_scenario.items():
        if name not in ordered:
            ordered[name] = row

    budget_ok = (
        n_neurons <= int(budget["max_neurons"])
        and n_synapses <= int(budget["max_synapses"])
        and over_budget == 0
    )

    return {
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "spike_count": int(round(avg_spikes)),
        "synops": int(round(avg_synops)),
        "latency_proxy_ms": round(steps * dt_ms, 3),
        "budget_ok": budget_ok,
        "n_neurons": n_neurons,
        "n_synapses": n_synapses,
        "n_test": len(test),
        "samples_over_spike_budget": over_budget,
        "metric_primary": project["task"].get("metric_primary", "f1"),
        "train_epochs": train_epochs,
        "train_epochs_ran": epochs_ran,
        "n_train": len(train),
        "backend": "numpy" if (_HAS_NUMPY and hidden._use_np) else "stdlib",
        "by_scenario": ordered,
        "by_scenario_mode": "split",
    }
