# Step B — live Synapse E5 export → Closed Sandbox

**Date:** 2026-07-29  
**Bench:** `synapse/benchmarks/results/2026-07-29-e5-brain-escalate.json` (**PASS**)  
**Exporter:** `sandbox/scripts/export_synapse_e5_fixture.py`  
**Diff JSON:** [`e5-live-export-diff.json`](e5-live-export-diff.json)

## Pipeline

```text
synapse/.venv  →  e5 bench.py  →  *-e5-brain-escalate.json
                                      ↓ export_synapse_e5_fixture.py
                         examples/synapse_e5_import/fixtures/e5-official.json
                                      ↓ closed-sandbox run
                                   metrics.json / report.md
```

```bash
# Synapse
cd ~/Projects/synapse
.venv/bin/python export/e5-brain-escalate/smoke.py
.venv/bin/python export/e5-brain-escalate/bench.py

# Neurolab
cd ~/Projects/neurolab
python3 sandbox/scripts/export_synapse_e5_fixture.py
cd sandbox && PYTHONPATH=src python -m closed_sandbox.cli run examples/synapse_e5_import/project.toml
```

## Live focus KPIs (`hard_or_low_score`)

| KPI | Frozen (pre) | Live bench | Δ |
|---|---:|---:|---:|
| accuracy / f1 | 0.856 | **0.8561** | +0.0001 |
| escalate_rate | 0.068 | **0.0682** | +0.0002 |
| oracle_accuracy | 0.89 | **0.8902** | +0.0002 |
| latency_proxy_ms (portable) | 0.44 | **0.4906** | +0.0506 |
| portable_pass | (assumed) | **true** | |
| escalate_policy_ok | (assumed) | **true** | |

Conclusion: CARD numbers were already honest; live export confirms them and wires **reproducible refresh**.

## DoD (B)

- [x] Torch env healthy (smoke OK, mid_backend=onnx)  
- [x] Official E5 bench PASS  
- [x] Exporter script  
- [x] Fixture updated (+ `.bak`)  
- [x] Sandbox `run` + before/after `diff`  
- [ ] Optional re-ask (skipped — deltas tiny; step A still valid)

## Next

- Cron/manual ritual: bench → export → sandbox run before demos  
- Outpost Gate: real escalate→chat on the 6.8% rows (beyond import)
