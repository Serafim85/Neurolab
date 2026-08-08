# Lab note — anomaly_v0 stress + train harden (2026-07-29)

## Can Neurolab + Synapse run “through” Closed Sandbox?

**Not as one binary today.** Stacks stay separate:

| Piece | Where it runs now |
|---|---|
| SNN design / anomaly demo | Closed Sandbox `snn_lif` (`sandbox/`) |
| Contour LLM (`ask`) | Neurolab hammer2 via Outpost — **already** wired in sandbox |
| Synapse ensembles / e5 escalate | Synapse lab (`export/e5-brain-escalate/`) — needs its torch venv |
| Unified synapse→brain product loop | Contract only (`BRAIN-BRIDGE.md`); Outpost Gate later |

**Practical today:**
1. Stress / improve SNN in sandbox (this note).  
2. `closed-sandbox ask` = Neurolab brain on sandbox metrics.  
3. Synapse benches stay in synapse; escalate flag is lab probe, not sandbox domain yet.

Next domain step (backlog): thin `synapse_export` plugin that maps Synapse CARD metrics → sandbox `metrics.json` schema — **not** started this session.

---

## Before / after (20 seeds, 0…19)

| | Before (8 ep, n_train=80) | After (20 ep + shuffle + n_train=120) |
|---|---|---|
| f1 mean | 0.817 | **0.898** |
| f1 stdev | 0.121 | **0.059** |
| f1 min | 0.429 | **0.765** |
| f1 max | 0.947 | 0.974 |
| budget_ok | 1.0 | **1.0** |

Raw summary: [`stress-anomaly-v0/summary.json`](stress-anomaly-v0/summary.json) · table: [`stress-anomaly-v0/report.md`](stress-anomaly-v0/report.md)

## Code changes

- `domains/snn_lif`: more data/epochs, shuffle, lr decay; optional `train_epochs` in `[network]`
- `engine`: always set `wall_ms` (sim latency stays `latency_proxy_ms`)
- `cli stress`: seed sweep → summary + per-seed JSON + markdown
- report.md shows `wall_ms`

## How to re-run

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli stress examples/anomaly_v0/project.toml \
  --n-seeds 20 --out reports/stress-anomaly-v0
PYTHONPATH=src:tests pytest -m "not integration" -q
```

## Open improvements

- Cut wall_ms (~7.5s/seed) without losing stability (vectorize / fewer steps)  
- Domain plugin for Synapse export metrics  
- Re-enable Synapse e5 smoke when torch env is healthy; then optional `ask` on escalate rows
