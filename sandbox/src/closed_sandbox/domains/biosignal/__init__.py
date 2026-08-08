"""Domain D3: biosignal — synthetic ECG/EEG-like → spike encode → classify.

Digital signals only (no clinical devices / no wet-lab). NL-ADR-023.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from closed_sandbox.domains.snn_lif.lif import LIFLayer, LIFParams
from closed_sandbox.manifest import ManifestError

DOMAIN_ID = "biosignal"

_KINDS = ("synthetic_ecg_v0", "synthetic_eeg_v0")
_ENCODERS = ("threshold",)

# Signal conditions (both labels kept so per-scenario F1 stays meaningful).
KNOWN_SCENARIOS = ("clean", "arrhythmia", "noisy")


def _scenario_params(scenario: str) -> tuple[float, float]:
    """Return (noise_scale, anomaly_boost) for a generative condition."""
    if scenario == "arrhythmia":
        return 1.0, 1.7
    if scenario == "noisy":
        return 3.2, 1.0
    # clean / rhythm (legacy)
    return 1.0, 1.0


def validate_project(project: dict[str, Any]) -> None:
    if project["project"]["domain"] != DOMAIN_ID:
        raise ManifestError(
            f"domain mismatch: expected {DOMAIN_ID}, got {project['project']['domain']}"
        )
    if "signal" not in project:
        raise ManifestError("biosignal requires [signal]")
    sig = project["signal"]
    kind = sig.get("kind")
    if kind not in _KINDS:
        raise ManifestError(f"[signal].kind must be one of {_KINDS}; got {kind!r}")
    encode = sig.get("encode", "threshold")
    if encode not in _ENCODERS:
        raise ManifestError(f"[signal].encode must be one of {_ENCODERS}; got {encode!r}")
    for key in ("n_channels", "n_samples"):
        if key not in sig:
            raise ManifestError(f"[signal] missing key: {key}")
    if "network" not in project:
        raise ManifestError("biosignal requires [network]")
    net = project["network"]
    for key in ("n_hidden", "n_outputs"):
        if key not in net:
            raise ManifestError(f"[network] missing key: {key}")
    if int(net["n_outputs"]) < 2:
        raise ManifestError("[network].n_outputs must be >= 2")
    if "budget" not in project:
        raise ManifestError("biosignal requires [budget]")
    for key in (
        "max_channels",
        "max_samples",
        "max_spikes_per_sample",
        "max_neurons",
        "max_synapses",
    ):
        if key not in project["budget"]:
            raise ManifestError(f"[budget] missing key: {key}")


def _synth_ecg(
    rng: np.random.Generator,
    *,
    n_samples: int,
    anomaly: bool,
    noise_scale: float = 1.0,
    anomaly_boost: float = 1.0,
) -> np.ndarray:
    t = np.linspace(0.0, 1.0, n_samples, endpoint=False)
    # Slow rhythm + QRS-like bumps.
    hr = 1.0 + 0.15 * rng.normal()
    base = 0.25 * np.sin(2 * np.pi * hr * t * 3.0)
    qrs = np.exp(-((t - 0.3) ** 2) / (2 * 0.008**2)) - 0.3 * np.exp(
        -((t - 0.35) ** 2) / (2 * 0.012**2)
    )
    wave = base + 0.9 * qrs + 0.05 * noise_scale * rng.normal(size=n_samples)
    if anomaly:
        # Ectopic burst / noise spike mid-window.
        mid = n_samples // 2
        width = max(3, n_samples // 20)
        wave[mid : mid + width] += anomaly_boost * (
            1.8 + 0.4 * rng.random(width)
        )
    return wave.astype(np.float64)


def _synth_eeg(
    rng: np.random.Generator,
    *,
    n_samples: int,
    anomaly: bool,
    noise_scale: float = 1.0,
    anomaly_boost: float = 1.0,
) -> np.ndarray:
    t = np.linspace(0.0, 1.0, n_samples, endpoint=False)
    alpha = 0.4 * np.sin(2 * np.pi * 10.0 * t)
    beta = 0.2 * np.sin(2 * np.pi * 20.0 * t + 0.3)
    wave = alpha + beta + 0.08 * noise_scale * rng.normal(size=n_samples)
    if anomaly:
        # High-amplitude transient (toy seizure-like burst).
        mid = n_samples // 3
        width = max(4, n_samples // 12)
        wave[mid : mid + width] += anomaly_boost * 1.5 * np.sin(
            2 * np.pi * 40.0 * t[mid : mid + width]
        )
    return wave.astype(np.float64)


def _make_trace(
    rng: np.random.Generator,
    *,
    kind: str,
    n_samples: int,
    anomaly: bool,
    scenario: str = "clean",
) -> np.ndarray:
    noise_scale, anomaly_boost = _scenario_params(scenario)
    if kind == "synthetic_ecg_v0":
        return _synth_ecg(
            rng,
            n_samples=n_samples,
            anomaly=anomaly,
            noise_scale=noise_scale,
            anomaly_boost=anomaly_boost,
        )
    return _synth_eeg(
        rng,
        n_samples=n_samples,
        anomaly=anomaly,
        noise_scale=noise_scale,
        anomaly_boost=anomaly_boost,
    )


def _threshold_encode(wave: np.ndarray, *, threshold: float) -> np.ndarray:
    """Binary spike train: 1 when |x| crosses threshold (rising)."""
    spikes = np.zeros_like(wave, dtype=np.float64)
    above = np.abs(wave) >= threshold
    rising = above & np.concatenate([[False], above[:-1] == False])  # noqa: E712
    spikes[rising] = 1.0
    # Also fire on strong absolute samples to keep rate alive.
    spikes[np.abs(wave) >= threshold * 1.5] = 1.0
    return spikes


def _f1_binary(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    acc = (tp + tn) / max(1, len(y_true))
    prec = tp / max(1, tp + fp)
    rec = tp / max(1, tp + fn)
    f1 = 0.0 if prec + rec == 0 else 2 * prec * rec / (prec + rec)
    return float(acc), float(f1)


def run(project: dict[str, Any], *, seed: int) -> dict[str, Any]:
    sig = project["signal"]
    net = project["network"]
    budget = project["budget"]

    kind = str(sig["kind"])
    encode = str(sig.get("encode", "threshold"))
    n_channels = int(sig["n_channels"])
    n_samples = int(sig["n_samples"])
    threshold = float(sig.get("threshold", 0.45))
    n_hidden = int(net["n_hidden"])
    n_outputs = int(net["n_outputs"])
    n_train = int(sig.get("n_train", 40))
    n_test = int(sig.get("n_test", 20))
    sim_steps = int(net.get("sim_steps", max(8, n_samples // 8)))

    scenario_names = list(project.get("sandbox", {}).get("scenarios") or [])
    if not scenario_names:
        scenario_names = list(KNOWN_SCENARIOS)
    n_test_per = max(
        4, int(sig.get("n_test_per_scenario", max(4, n_test // len(scenario_names))))
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

    hidden = LIFLayer(n_hidden, n_hidden, seed=seed, params=LIFParams(), weight_scale=0.5)
    readout = LIFLayer(n_hidden, n_outputs, seed=seed + 1, params=LIFParams(), weight_scale=0.5)

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
        pred = int(np.argmax(o_counts))
        return pred, spikes_total, synops

    # Light supervised nudge on readout weights.
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
        "signal_kind": kind,
        "signal_encode": encode,
        "signal_n_channels": n_channels,
        "signal_n_samples": n_samples,
        "signal_threshold": threshold,
        "n_neurons": n_neurons,
        "n_synapses": n_synapses,
        "n_train": n_train,
        "n_test": n_test_total,
        "signal_disclaimer": (
            "synthetic biosignal toy — not clinical ECG/EEG; not a medical device"
        ),
        "seed": seed,
        "by_scenario": by_scenario,
        "by_scenario_mode": "split",
    }
