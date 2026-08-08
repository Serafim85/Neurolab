# Escalate → Outpost chat (lab Gate probe)

**Date:** 2026-07-29  
**Synapse evidence:** `~/Projects/synapse/benchmarks/results/2026-07-29-e5-outpost-brain.md`  
**Code:** `synapse/export/e5-brain-escalate/{outpost_brain.py,bench_outpost.py}` · `brain="outpost"`

## What ran

```text
DVS test (264) → E5 cascade → escalate ~6.8% (18 rows)
                              → HTTP Outpost hammer2 :8098
                              → JSON {class_id} → replace if parse OK
```

| Brain | Acc | Notes |
|---|---|---|
| stub | 0.8561 | cascade only |
| **outpost** | **0.8561** | 18 calls, **18/18 parse OK**, 0 class changes |
| oracle | 0.8902 | upper bound |

## Verdict

- **Wiring ✅** — Synapse escalate → Neurolab/Outpost chat → structured reply.  
- **Accuracy ❌ lift** — Tiny agreed with cascade top-1 on all escalate rows (Δ=0).  
- Expected: chat on top-k logits ≠ vision brain; oracle gap **3.4 pp** remains.

## How to re-run

```bash
# Outpost
nohup ~/Projects/AI-Platform-Vision/target/release/sovereignd \
  ~/Projects/neurolab/config/sovereign.sandbox-ask.toml >/tmp/sandbox-ask-e5.log 2>&1 &

cd ~/Projects/synapse
.venv/bin/python export/e5-brain-escalate/bench_outpost.py
```

## Next (not done)

- Better escalate payload (calibrated probs / uncertainty features) or Mid brain  
- Commercial Gate: audit + governor around escalate calls (SOW)  
- Do **not** claim Tiny closes the oracle gap
