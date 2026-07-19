# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **Quality bar** | `outpost-tiny-v0` · **15/20** |
| **Latest experiment** | `outpost-tiny-v1` (v1.1) · **14/20** |
| **Base** | Qwen2.5-3B-Instruct · Apache-2.0 · dense (not MoE) |

## GGUF (this machine)

| ID | Path | SHA-256 | Eval |
|---|---|---|---|
| v0 | `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | `405b4443…ce27a7` | **15/20** |
| v1.1 | `artifacts/outpost-tiny-v1.Q4_K_M.gguf` | `e5dfa81f…949c` | 14/20 |

## Eval sheets

- `eval/results/tiny-v0-vs-baseline.md`
- `eval/results/tiny-v1-vs-baseline.md` (conflict data · 12/20)
- `eval/results/tiny-v1.1-vs-baseline.md` (**14/20**)

## Train (v1.1)

| | |
|---|---|
| Data | `datasets/tiny-lora-v1/` · 74 deduped |
| Run | `artifacts/runs/20260719-mps-v1.1` |
| Recipe | MPS float16 · lr=8e-5 · max_grad_norm=0.3 · 2 epochs · NanGuard |
| Note | lr=1.2e-4 NaN on MPS — do not use |

## Smoke

```bash
# quality bar
sovereignd config/sovereign.tiny-v0.toml   # :8091
# experiment
sovereignd config/sovereign.tiny-v1.toml   # :8092
```
