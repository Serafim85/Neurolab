"""LIF neuron layer — numpy fast path, stdlib fallback."""

from __future__ import annotations

import random
from dataclasses import dataclass

try:
    import numpy as np

    _HAS_NUMPY = True
except ImportError:  # pragma: no cover
    np = None  # type: ignore[assignment]
    _HAS_NUMPY = False


@dataclass
class LIFParams:
    v_th: float = 1.0
    v_reset: float = 0.0
    tau: float = 10.0
    dt: float = 1.0
    r: float = 1.0


class LIFLayer:
    """Vector of LIF neurons driven by weighted input currents."""

    def __init__(
        self,
        n_in: int,
        n_out: int,
        *,
        seed: int,
        params: LIFParams | None = None,
        weight_scale: float = 0.35,
    ) -> None:
        self.n_in = n_in
        self.n_out = n_out
        self.params = params or LIFParams()
        rng = random.Random(seed)
        if _HAS_NUMPY:
            rs = np.random.RandomState(seed)
            self.weights_np = rs.uniform(
                -weight_scale, weight_scale, size=(n_out, n_in)
            ).astype(np.float64)
            self.v_np = np.zeros(n_out, dtype=np.float64)
            # Keep list view in sync for rare list-based callers / tests
            self.weights = self.weights_np.tolist()
            self.v = self.v_np.tolist()
            self._use_np = True
        else:  # pragma: no cover
            self.weights = [
                [rng.uniform(-weight_scale, weight_scale) for _ in range(n_in)]
                for _ in range(n_out)
            ]
            self.v = [0.0] * n_out
            self.weights_np = None
            self.v_np = None
            self._use_np = False

    def reset(self) -> None:
        if self._use_np:
            self.v_np.fill(0.0)
            self.v = self.v_np.tolist()
        else:  # pragma: no cover
            self.v = [0.0] * self.n_out

    def sync_weights_from_list(self) -> None:
        """After in-place list weight updates, refresh numpy buffer."""
        if self._use_np:
            self.weights_np = np.asarray(self.weights, dtype=np.float64)

    def step(self, inputs: list[float] | "np.ndarray") -> list[int]:
        """One timestep; returns binary spikes for each neuron."""
        p = self.params
        decay = 1.0 - (p.dt / p.tau)
        scale = p.r * p.dt
        if self._use_np:
            x = np.asarray(inputs, dtype=np.float64)
            i_syn = self.weights_np @ x
            self.v_np *= decay
            self.v_np += scale * i_syn
            spiked = self.v_np >= p.v_th
            spikes = spiked.astype(np.int64)
            self.v_np[spiked] = p.v_reset
            self.v = self.v_np.tolist()
            return spikes.tolist()

        spikes = [0] * self.n_out  # pragma: no cover
        for j in range(self.n_out):
            i_syn = sum(self.weights[j][k] * inputs[k] for k in range(self.n_in))
            self.v[j] = decay * self.v[j] + scale * i_syn
            if self.v[j] >= p.v_th:
                spikes[j] = 1
                self.v[j] = p.v_reset
        return spikes

    def step_np(self, inputs: "np.ndarray") -> "np.ndarray":
        """Numpy-native step; returns int spike vector."""
        if not self._use_np:
            return np.asarray(self.step(inputs.tolist()), dtype=np.int64)
        p = self.params
        decay = 1.0 - (p.dt / p.tau)
        scale = p.r * p.dt
        i_syn = self.weights_np @ inputs
        self.v_np *= decay
        self.v_np += scale * i_syn
        spiked = self.v_np >= p.v_th
        spikes = spiked.astype(np.int64)
        self.v_np[spiked] = p.v_reset
        return spikes


def count_synops(n_in: int, spikes: list[int] | "np.ndarray") -> int:
    """Proxy synaptic operations: each spike fans in from all inputs (dense)."""
    return int(n_in * int(sum(spikes)))
