# chip-estimate-v0 — D1 `neuro_chip`

Rough **map / estimate** of an SNN topology onto a named neuromorphic target.
Not fab, not PDK, not measured silicon Joules (NL-ADR-020).

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli run examples/chip_estimate_v0/project.toml
```

| Field | Meaning |
|---|---|
| `chip_target` | `generic_neuromorphic_v0` |
| `chip_area_mm2` / `chip_power_mw` | proxy estimates |
| `chip_fit_score` | headroom vs `[budget]` chip caps |
| `source_metrics` | optional prior `snn_lif` metrics JSON |

Refresh fixture from a live D0 run if needed:

```bash
PYTHONPATH=src python -m closed_sandbox.cli run examples/anomaly_v0/project.toml --seed 42
# copy out/metrics.json → fixtures/anomaly-v0-metrics.json (keys used: f1, spikes, synops)
```
