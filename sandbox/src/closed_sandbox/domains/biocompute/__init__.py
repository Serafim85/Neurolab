"""Domain D2: digital biocompute — toy gene-regulatory / boolean circuit (sim only).

No wet-lab, no culture, no organoids. Metrics use bio_* resource proxies.
NL-ADR-022.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from closed_sandbox.manifest import ManifestError

DOMAIN_ID = "biocompute"

_KINDS = ("boolean_grn_v0",)

# Input-pattern conditions (both labels kept via majority task).
KNOWN_SCENARIOS = ("balanced", "sparse", "dense")


def _input_bias(scenario: str) -> float:
    """P(bit=1) for synthetic inputs under a scenario condition."""
    if scenario == "sparse":
        return 0.18
    if scenario == "dense":
        return 0.82
    # balanced / grn (legacy)
    return 0.5


def validate_project(project: dict[str, Any]) -> None:
    if project["project"]["domain"] != DOMAIN_ID:
        raise ManifestError(
            f"domain mismatch: expected {DOMAIN_ID}, got {project['project']['domain']}"
        )
    if "circuit" not in project:
        raise ManifestError("biocompute requires [circuit]")
    circ = project["circuit"]
    kind = circ.get("kind")
    if kind not in _KINDS:
        raise ManifestError(f"[circuit].kind must be one of {_KINDS}; got {kind!r}")
    for key in ("n_genes", "n_inputs", "n_outputs", "steps"):
        if key not in circ:
            raise ManifestError(f"[circuit] missing key: {key}")
    if int(circ["n_inputs"]) + int(circ["n_outputs"]) > int(circ["n_genes"]):
        raise ManifestError(
            "[circuit] n_genes must be >= n_inputs + n_outputs "
            "(inputs/outputs occupy gene slots)"
        )
    if "budget" not in project:
        raise ManifestError("biocompute requires [budget]")
    for key in ("max_genes", "max_edges", "max_steps", "max_bio_resource"):
        if key not in project["budget"]:
            raise ManifestError(f"[budget] missing key: {key}")


def _build_edges(
    rng: np.random.Generator, *, n_genes: int, n_inputs: int, max_edges: int
) -> np.ndarray:
    """Sparse signed regulatory matrix W[j,i]: i → j (inputs have no incoming)."""
    w = np.zeros((n_genes, n_genes), dtype=np.float64)
    candidates = [
        (j, i)
        for j in range(n_inputs, n_genes)
        for i in range(n_genes)
        if i != j
    ]
    rng.shuffle(candidates)
    n_edges = min(max_edges, max(1, len(candidates) // 3))
    for j, i in candidates[:n_edges]:
        w[j, i] = float(rng.choice([-1.0, 1.0]))
    return w


def _simulate(
    w: np.ndarray,
    x_in: np.ndarray,
    *,
    n_inputs: int,
    steps: int,
) -> np.ndarray:
    """Discrete threshold GRN; clamp inputs each step."""
    n_genes = w.shape[0]
    state = np.zeros(n_genes, dtype=np.float64)
    state[:n_inputs] = x_in
    for _ in range(steps):
        drive = w @ state
        nxt = (drive > 0.0).astype(np.float64)
        nxt[:n_inputs] = x_in
        state = nxt
    return state


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


def _make_dataset(
    rng: np.random.Generator,
    *,
    n_inputs: int,
    n_train: int,
    n_test_per_scenario: int,
    scenarios: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray, np.ndarray, list[str]]:
    """Synthetic binary task: label = majority of input bits (tie → 1).

    Scenarios change P(bit=1); train mixes conditions, test is per-scenario.
    """

    def labels(x: np.ndarray) -> np.ndarray:
        s = x.sum(axis=1)
        return (s >= (n_inputs / 2.0)).astype(np.int64)

    def draw(n: int, p1: float) -> np.ndarray:
        return (rng.random((n, n_inputs)) < p1).astype(np.float64)

    x_train_parts = []
    scen_train: list[str] = []
    for i in range(n_train):
        sc = scenarios[i % len(scenarios)]
        x_train_parts.append(draw(1, _input_bias(sc))[0])
        scen_train.append(sc)
    x_train = np.stack(x_train_parts, axis=0)

    x_test_parts = []
    scen_test: list[str] = []
    for sc in scenarios:
        block = draw(n_test_per_scenario, _input_bias(sc))
        x_test_parts.append(block)
        scen_test.extend([sc] * n_test_per_scenario)
    x_test = np.concatenate(x_test_parts, axis=0)

    return (
        x_train,
        labels(x_train),
        scen_train,
        x_test,
        labels(x_test),
        scen_test,
    )


def _bucket_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    steps: int,
    n_genes: int,
    activity: float = 1.0,
) -> dict[str, Any]:
    n = int(len(y_true))
    if n == 0:
        return {"n": 0, "accuracy": 0.0, "f1": 0.0, "spike_count": 0, "synops": 0}
    accuracy, f1 = _f1_binary(y_true, y_pred)
    return {
        "n": n,
        "accuracy": round(accuracy, 4),
        "f1": round(f1, 4),
        "spike_count": 0,
        # Activity-scaled ops proxy so sparse/dense rows differ even if F1 ties.
        "synops": int(n_genes * steps * n * max(0.25, activity)),
    }


def run(project: dict[str, Any], *, seed: int) -> dict[str, Any]:
    circ = project["circuit"]
    budget = project["budget"]
    n_genes = int(circ["n_genes"])
    n_inputs = int(circ["n_inputs"])
    n_outputs = int(circ["n_outputs"])
    steps = int(circ["steps"])
    n_train = int(circ.get("n_train", 64))
    n_test = int(circ.get("n_test", 32))

    scenario_names = list(project.get("sandbox", {}).get("scenarios") or [])
    if not scenario_names:
        scenario_names = list(KNOWN_SCENARIOS)
    n_test_per = max(4, int(circ.get("n_test_per_scenario", max(4, n_test // len(scenario_names)))))

    rng = np.random.default_rng(seed)
    max_edges_cap = int(budget["max_edges"])
    w = _build_edges(
        rng, n_genes=n_genes, n_inputs=n_inputs, max_edges=max_edges_cap
    )
    # Soft inductive bias for majority task: each output gene sees all inputs (+).
    for o in range(n_genes - n_outputs, n_genes):
        for i in range(n_inputs):
            w[o, i] = 1.0
    n_edges = int(np.count_nonzero(w))

    x_train, y_train, _sc_tr, x_test, y_test, scen_test = _make_dataset(
        rng,
        n_inputs=n_inputs,
        n_train=n_train,
        n_test_per_scenario=n_test_per,
        scenarios=scenario_names,
    )

    # Readout: majority of designated output genes after dynamics.
    out_slice = slice(n_genes - n_outputs, n_genes)

    def predict(x_batch: np.ndarray) -> np.ndarray:
        preds = []
        for row in x_batch:
            state = _simulate(w, row, n_inputs=n_inputs, steps=steps)
            vote = float(state[out_slice].mean())
            preds.append(1 if vote >= 0.5 else 0)
        return np.asarray(preds, dtype=np.int64)

    y_hat_train = predict(x_train)
    acc_tr, f1_tr = _f1_binary(y_train, y_hat_train)
    y_hat = predict(x_test)
    accuracy, f1 = _f1_binary(y_test, y_hat)

    by_scenario: dict[str, Any] = {}
    for name in scenario_names:
        mask = np.asarray([s == name for s in scen_test], dtype=bool)
        activity = float(x_test[mask].mean()) if mask.any() else 1.0
        by_scenario[name] = _bucket_metrics(
            y_test[mask],
            y_hat[mask],
            steps=steps,
            n_genes=n_genes,
            activity=0.5 + activity,
        )

    # Resource proxy: regulatory evaluations (not ATP Joules).
    n_test_total = int(len(y_test))
    bio_resource = int(n_genes * steps * (n_train + n_test_total))
    synops = int(n_genes * steps * n_test_total)
    spike_count = 0

    budget_ok = (
        n_genes <= int(budget["max_genes"])
        and n_edges <= int(budget["max_edges"])
        and steps <= int(budget["max_steps"])
        and bio_resource <= int(budget["max_bio_resource"])
    )

    primary = project.get("task", {}).get("metric_primary", "accuracy")

    return {
        "accuracy": round(accuracy, 4),
        "f1": round(f1, 4),
        "spike_count": spike_count,
        "synops": synops,
        "latency_proxy_ms": round(steps * 0.01, 4),
        "budget_ok": budget_ok,
        "metric_primary": primary,
        "bio_kind": str(circ["kind"]),
        "bio_n_genes": n_genes,
        "bio_n_edges": n_edges,
        "bio_n_inputs": n_inputs,
        "bio_n_outputs": n_outputs,
        "bio_steps": steps,
        "bio_circuit_size": n_genes,
        "bio_resource_proxy": bio_resource,
        "bio_train_f1": round(f1_tr, 4),
        "bio_disclaimer": (
            "digital GRN toy — not wet-lab; bio_resource_proxy is sim ops, not ATP Joules"
        ),
        "n_train": n_train,
        "n_test": n_test_total,
        "seed": seed,
        "by_scenario": by_scenario,
        "by_scenario_mode": "split",
    }
