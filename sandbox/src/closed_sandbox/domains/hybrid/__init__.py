"""Domain D4: hybrid — bio front-end (synthetic signal) → silicon SNN backend.

Composition of D3 encode + D0 LIF classify. Digital only (NL-ADR-024).
"""

from __future__ import annotations

from typing import Any

import numpy as np

from closed_sandbox.domains.biosignal import (
    _KINDS as _FRONT_KINDS,
    _f1_binary,
    _make_trace,
    _threshold_encode,
)
from closed_sandbox.domains.snn_lif.lif import LIFLayer, LIFParams
from closed_sandbox.manifest import ManifestError

DOMAIN_ID = "hybrid"
METRICS_FAMILY = "snn"

_BACKENDS = ("snn_lif",)
_ENCODERS = ("threshold",)
KNOWN_SCENARIOS = ("clean", "arrhythmia", "noisy")


def validate_project(project: dict[str, Any]) -> None:
    if project["project"]["domain"] != DOMAIN_ID:
        raise ManifestError(
            f"domain mismatch: expected {DOMAIN_ID}, got {project['project']['domain']}"
        )
    if "front" not in project:
        raise ManifestError("hybrid requires [front]")
    front = project["front"]
    kind = front.get("kind")
    if kind not in _FRONT_KINDS:
        raise ManifestError(
            f"[front].kind must be one of {tuple(_FRONT_KINDS)}; got {kind!r}"
        )
    encode = front.get("encode", "threshold")
    if encode not in _ENCODERS:
        raise ManifestError(f"[front].encode must be one of {_ENCODERS}; got {encode!r}")
    for key in ("n_channels", "n_samples"):
        if key not in front:
            raise ManifestError(f"[front] missing key: {key}")

    if "backend" not in project:
        raise ManifestError("hybrid requires [backend]")
    back = project["backend"]
    if back.get("kind") not in _BACKENDS:
        raise ManifestError(
            f"[backend].kind must be one of {_BACKENDS}; got {back.get('kind')!r}"
        )
    for key in ("n_hidden", "n_outputs"):
        if key not in back:
            raise ManifestError(f"[backend] missing key: {key}")
    if int(back["n_outputs"]) < 2:
        raise ManifestError("[backend].n_outputs must be >= 2")

    if "budget" not in project:
        raise ManifestError("hybrid requires [budget]")
    for key in (
        "max_channels",
        "max_samples",
        "max_spikes_per_sample",
        "max_neurons",
        "max_synapses",
    ):
        if key not in project["budget"]:
            raise ManifestError(f"[budget] missing key: {key}")


def run(project: dict[str, Any], *, seed: int) -> dict[str, Any]:
    front = project["front"]
    back = project["backend"]
    budget = project["budget"]

    kind = str(front["kind"])
    encode = str(front.get("encode", "threshold"))
    n_channels = int(front["n_channels"])
    n_samples = int(front["n_samples"])
    threshold = float(front.get("threshold", 0.45))
    n_train = int(front.get("n_train", 40))
    n_test = int(front.get("n_test", 20))

    n_hidden = int(back["n_hidden"])
    n_outputs = int(back["n_outputs"])
    sim_steps = int(back.get("sim_steps", max(8, n_samples // 8)))
    backend_kind = str(back["kind"])

    scenario_names = list(project.get("sandbox", {}).get("scenarios") or [])
    if not scenario_names:
        scenario_names = list(KNOWN_SCENARIOS)
    n_test_per = max(
        4,
        int(front.get("n_test_per_scenario", max(4, n_test // len(scenario_names)))),
    )

    rng = np.random.default_rng(seed)

    def make_xy(
        n: int, *, scenarios: list[str], per_scenario: bool
    ) -> tuple[list[np.ndarray], np.ndarray, list[str]]:
        xs: list[np.ndarray] = []
        ys: list[int] = []
        scens: list[str] = []
        if per_scenario:
            plan = [(sc, i) for sc in scenarios for i in range(n)]
        else:
            plan = [(scenarios[i % len(scenarios)], i) for i in range(n)]
        for sc, i in plan:
            anomaly = bool(i % 2)
            chans = []
            for _c in range(n_channels):
                wave = _make_trace(
                    rng, kind=kind, n_samples=n_samples, anomaly=anomaly, scenario=sc
                )
                chans.append(_threshold_encode(wave, threshold=threshold))
            stacked = np.stack(chans, axis=0)
            bins = np.array_split(stacked.mean(axis=0), n_hidden)
            feat = np.array(
                [float(b.mean()) if len(b) else 0.0 for b in bins], dtype=np.float64
            )
            xs.append(feat)
            ys.append(1 if anomaly else 0)
            scens.append(sc)
        return xs, np.asarray(ys, dtype=np.int64), scens

    x_train, y_train, _ = make_xy(n_train, scenarios=scenario_names, per_scenario=False)
    x_test, y_test, scen_test = make_xy(
        n_test_per, scenarios=scenario_names, per_scenario=True
    )

    # Silicon backend: same LIF stack as D0/D3.
    hidden = LIFLayer(
        n_hidden, n_hidden, seed=seed, params=LIFParams(), weight_scale=0.5
    )
    readout = LIFLayer(
        n_hidden, n_outputs, seed=seed + 1, params=LIFParams(), weight_scale=0.5
    )

    def predict_one(feat: np.ndarray) -> tuple[int, int, int]:
        hidden.reset()
        readout.reset()
        spikes_total = 0
        synops = 0
        o_counts = np.zeros(n_outputs, dtype=np.int64)
        for _ in range(sim_steps):
            h_spikes = hidden.step_np(feat)
            hs = int(h_spikes.sum())
            spikes_total += hs
            synops += hs * n_outputs
            o_spikes = readout.step_np(h_spikes.astype(np.float64))
            o_counts += o_spikes
            spikes_total += int(o_spikes.sum())
        return int(np.argmax(o_counts)), spikes_total, synops

    for epoch in range(4):
        err = 0
        for feat, y in zip(x_train, y_train, strict=True):
            pred, _, _ = predict_one(feat)
            if pred != int(y):
                err += 1
                j = int(rng.integers(0, n_hidden))
                if readout.weights_np is not None:
                    readout.weights_np[:, j] *= -1.0 if epoch % 2 == 0 else 1.08
                    readout.weights = readout.weights_np.tolist()
        if err <= max(1, n_train // 10):
            break

    preds: list[int] = []
    spikes_list: list[int] = []
    synops_list: list[int] = []
    for feat in x_test:
        pred, sp, sy = predict_one(feat)
        preds.append(pred)
        spikes_list.append(sp)
        synops_list.append(sy)

    y_hat = np.asarray(preds, dtype=np.int64)
    accuracy, f1 = _f1_binary(y_test, y_hat)
    n_test_total = int(len(y_test))
    spike_count = int(round(sum(spikes_list) / max(1, n_test_total)))
    synops = int(round(sum(synops_list) / max(1, n_test_total)))

    by_scenario: dict[str, Any] = {}
    for name in scenario_names:
        idx = [i for i, s in enumerate(scen_test) if s == name]
        if not idx:
            by_scenario[name] = {
                "n": 0,
                "f1": 0.0,
                "accuracy": 0.0,
                "spike_count": 0,
                "synops": 0,
            }
            continue
        yt = y_test[idx]
        yp = y_hat[idx]
        acc_s, f1_s = _f1_binary(yt, yp)
        n_s = len(idx)
        by_scenario[name] = {
            "n": n_s,
            "f1": round(f1_s, 4),
            "accuracy": round(acc_s, 4),
            "spike_count": int(round(sum(spikes_list[i] for i in idx) / n_s)),
            "synops": int(round(sum(synops_list[i] for i in idx) / n_s)),
        }

    n_neurons = n_hidden + n_outputs
    n_synapses = n_hidden * n_hidden + n_hidden * n_outputs

    budget_ok = (
        n_channels <= int(budget["max_channels"])
        and n_samples <= int(budget["max_samples"])
        and spike_count <= int(budget["max_spikes_per_sample"])
        and n_neurons <= int(budget["max_neurons"])
        and n_synapses <= int(budget["max_synapses"])
    )

    primary = project.get("task", {}).get("metric_primary", "f1")

    return {
        "accuracy": round(accuracy, 4),
        "f1": round(f1, 4),
        "spike_count": spike_count,
        "synops": synops,
        "latency_proxy_ms": round(sim_steps * 0.05, 4),
        "budget_ok": budget_ok,
        "metric_primary": primary,
        "hybrid_front": kind,
        "hybrid_front_encode": encode,
        "hybrid_backend": backend_kind,
        "hybrid_pipeline": f"{kind}+{encode} → {backend_kind}",
        "signal_n_channels": n_channels,
        "signal_n_samples": n_samples,
        "n_neurons": n_neurons,
        "n_synapses": n_synapses,
        "n_train": n_train,
        "n_test": n_test_total,
        "hybrid_disclaimer": (
            "digital hybrid composition — bio front is synthetic; "
            "silicon backend is LIF sim; not wet-lab / not clinical"
        ),
        "seed": seed,
        "by_scenario": by_scenario,
        "by_scenario_mode": "split",
    }
