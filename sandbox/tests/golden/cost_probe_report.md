# Sandbox report — cost-probe

- domain: `cost_probe_test`
- seed: `7`
- primary (`fit_score`): **0.75**
- latency_proxy_ms: `1.5`
- wall_ms: `0.0`
- budget_ok: **True**

## Resource economy (v0)

North star proxies — quality under event cost. Not bio-joules (see `docs/NORTH-STAR-BUILD.md` §4).

- quality_per_unit_cost [`fit_score` per `unit_cost_eur` (EUR)]: `0.06`
- budget_ok: **True**

## Per scenario

| scenario | n | fit_score | unit_cost_eur | latency_proxy_ms | budget_ok |
|---|---:|---:|---:|---:|---:|
| baseline | 2 | 0.75 | 12.5 | 1.5 | True |
| stretch | 2 | 0.75 | 12.5 | 1.5 | True |

## Raw metrics

```json
{
  "budget_ok": true,
  "by_scenario": {
    "baseline": {
      "budget_ok": true,
      "fit_score": 0.75,
      "latency_proxy_ms": 1.5,
      "n": 2,
      "unit_cost_eur": 12.5
    },
    "stretch": {
      "budget_ok": true,
      "fit_score": 0.75,
      "latency_proxy_ms": 1.5,
      "n": 2,
      "unit_cost_eur": 12.5
    }
  },
  "by_scenario_mode": "stub",
  "domain": "cost_probe_test",
  "economy_cost_key": "unit_cost_eur",
  "economy_cost_unit": "EUR",
  "estimate_disclaimer": "lab cost proxy \u2014 not a quote",
  "fit_score": 0.75,
  "latency_proxy_ms": 1.5,
  "metric_primary": "fit_score",
  "n_test": 2,
  "project_id": "cost-probe",
  "quality_per_unit_cost": 0.06,
  "seed": 7,
  "unit_cost_eur": 12.5,
  "wall_ms": 0.0
}
```
