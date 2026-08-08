"""Synthetic 1D anomaly windows for D0 demos (no external downloads).

Scenarios are generative *conditions* (not single-class buckets):
- nominal — low noise
- anomaly — stronger mid-window bumps when label=1
- noise — high noise (harder SNR)

Each scenario keeps both labels so per-scenario F1 stays meaningful.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

KNOWN_SCENARIOS = ("nominal", "anomaly", "noise")


@dataclass
class Sample:
    features: list[float]
    label: int  # 0 = nominal class, 1 = anomaly class
    scenario: str


def _mode_params(scenario: str) -> tuple[float, float]:
    """Return (noise_sigma, anomaly_amplitude) for a scenario condition."""
    if scenario == "anomaly":
        return 0.08, 1.45
    if scenario == "noise":
        return 0.38, 0.95
    # nominal (default for unknown names)
    return 0.05, 0.85


def _window(
    rng: random.Random,
    *,
    anomaly: bool,
    n_features: int,
    scenario: str,
) -> list[float]:
    noise_sigma, anomaly_amp = _mode_params(scenario)
    phase = rng.random() * 2 * math.pi
    xs: list[float] = []
    for t in range(n_features):
        base = math.sin(2 * math.pi * t / max(n_features - 1, 1) + phase)
        noise = rng.gauss(0.0, noise_sigma)
        val = base + noise
        if anomaly and n_features // 3 <= t <= 2 * n_features // 3:
            val += rng.choice([-1.0, 1.0]) * (anomaly_amp + rng.random() * 0.4)
        xs.append(val)
    return xs


def make_dataset(
    *,
    seed: int,
    n_features: int,
    scenarios: list[str] | tuple[str, ...] | None = None,
    n_train: int = 120,
    n_test_per_scenario: int = 14,
) -> tuple[list[Sample], list[Sample]]:
    names = list(scenarios) if scenarios else list(KNOWN_SCENARIOS)
    if not names:
        names = list(KNOWN_SCENARIOS)
    for name in names:
        if name not in KNOWN_SCENARIOS:
            # Unknown names fall back to nominal generative params.
            pass

    rng = random.Random(seed)
    train: list[Sample] = []
    for i in range(n_train):
        scenario = names[i % len(names)]
        anomaly = i % 2 == 1
        train.append(
            Sample(
                features=_window(
                    rng, anomaly=anomaly, n_features=n_features, scenario=scenario
                ),
                label=1 if anomaly else 0,
                scenario=scenario,
            )
        )

    test: list[Sample] = []
    for scenario in names:
        for i in range(n_test_per_scenario):
            anomaly = i % 2 == 1
            test.append(
                Sample(
                    features=_window(
                        rng,
                        anomaly=anomaly,
                        n_features=n_features,
                        scenario=scenario,
                    ),
                    label=1 if anomaly else 0,
                    scenario=scenario,
                )
            )
    return train, test
