# Sandbox report — anomaly-v0

- domain: `snn_lif`
- seed: `42`
- primary (`f1`): **0.7368**
- accuracy: `0.7619`
- spike_count (avg): `327`
- synops (avg): `6022`
- latency_proxy_ms: `24.0`
- wall_ms: `0.0`
- budget_ok: **True**

## Resource economy (v0)

North star proxies — quality under event cost. Not bio-joules (see `docs/NORTH-STAR-BUILD.md` §4).

- quality_per_kspike: `2.253211`
- quality_per_ksynop: `0.122351`
- budget_ok: **True**

## Per scenario

| scenario | n | f1 | accuracy | spike_count | synops |
|---|---:|---:|---:|---:|---:|
| nominal | 14 | 0.7273 | 0.7857 | 329 | 6003 |
| anomaly | 14 | 0.9231 | 0.9286 | 323 | 5990 |
| noise | 14 | 0.5714 | 0.5714 | 328 | 6074 |

## Raw metrics

```json
{
  "accuracy": 0.7619,
  "backend": "numpy",
  "budget_ok": true,
  "by_scenario": {
    "anomaly": {
      "accuracy": 0.9286,
      "f1": 0.9231,
      "n": 14,
      "spike_count": 323,
      "synops": 5990
    },
    "noise": {
      "accuracy": 0.5714,
      "f1": 0.5714,
      "n": 14,
      "spike_count": 328,
      "synops": 6074
    },
    "nominal": {
      "accuracy": 0.7857,
      "f1": 0.7273,
      "n": 14,
      "spike_count": 329,
      "synops": 6003
    }
  },
  "by_scenario_mode": "split",
  "domain": "snn_lif",
  "f1": 0.7368,
  "latency_proxy_ms": 24.0,
  "metric_primary": "f1",
  "n_neurons": 66,
  "n_synapses": 1152,
  "n_test": 42,
  "n_train": 120,
  "project_id": "anomaly-v0",
  "quality_per_kspike": 2.253211,
  "quality_per_ksynop": 0.122351,
  "samples_over_spike_budget": 0,
  "seed": 42,
  "spike_count": 327,
  "synops": 6022,
  "train_epochs": 20,
  "train_epochs_ran": 20,
  "wall_ms": 0.0
}
```
