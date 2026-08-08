# Lab note — speed + Synapse import (2026-07-29 evening)

## Speed (anomaly_v0, 20 seeds)

| | Prior stress | This pass |
|---|---|---|
| wall_ms mean | ~7482 | **~264** (~28×) |
| f1 mean ± stdev | 0.898 ± 0.059 | **0.932 ± 0.044** |
| f1 min | 0.765 | **0.833** |
| budget_ok | 1.0 | 1.0 |
| unit tests | 12 | **14** |

Levers: numpy LIF matmul, train without synops accounting, early-stop at train acc ≥0.98.

Raw: [`stress-anomaly-v0-fast/summary.json`](stress-anomaly-v0-fast/summary.json)

## Synapse through sandbox (thin)

New domain **`synapse_import`**: loads frozen JSON from Synapse CARD/bench — **no torch**.

```bash
PYTHONPATH=src python -m closed_sandbox.cli run examples/synapse_e5_import/project.toml
# → accuracy 0.856, escalate_rate 0.068, oracle_accuracy 0.89
```

Then same `diff` / `ask` path as SNN projects (ask still needs Outpost).

Still **not** a live Synapse runtime inside sandbox. Refresh fixture when Synapse torch env is healthy.

## How stacks meet now

```text
Synapse bench → JSON fixture → sandbox synapse_import → metrics/report
sandbox snn_lif → metrics/report
                    ↓
              closed-sandbox ask → Neurolab hammer2 (Outpost)
```
