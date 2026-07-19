# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **ID (quality bar)** | `outpost-tiny-v0` |
| **ID (experiment)** | `outpost-tiny-v1` |
| **Status** | **v0 lab GGUF** eval **15/20** · **v1** GGUF ready but eval **12/20** (keep v0) |
| **Architecture** | dense decoder-only (**not** MoE) |
| **Base (LOCKED)** | **Qwen2.5-3B-Instruct** · Apache-2.0 |
| **Role** | general RU/EN chat, 2nd slot, Workstation Lite |

## Artifacts (this machine)

| Artifact | Path | SHA-256 (prefix) |
|---|---|---|
| Base GGUF | `artifacts/base/Qwen2.5-3B-Instruct-Q4_K_M.gguf` | `d44e2c5d…` |
| **Tiny-v0 GGUF** | `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | `405b4443…ce27a7` |
| Tiny-v1 GGUF | `artifacts/outpost-tiny-v1.Q4_K_M.gguf` | `1de15252…d55430` |
| v0 adapter | `artifacts/runs/20260719-mps-e1/adapter` | |
| v1 adapter | `artifacts/runs/20260719-mps-v1-e1/adapter` | |

## Eval

| Model | Full 10 | Notes |
|---|---|---|
| Base Qwen 3B | 14/16 (8-prompt) | |
| Tiny-v0 | **15/20** | refuse↑ |
| Tiny-v1 e2 | **12/20** | short answers; clarify still wrong |

Sheets: `eval/results/tiny-v0-vs-baseline.md` · `eval/results/tiny-v1-vs-baseline.md`

## Data

| Set | Path | Notes |
|---|---|---|
| v0 | `datasets/tiny-lora-v0/` | 44 |
| v1 | `datasets/tiny-lora-v1/` | **74** after user-prompt dedupe (extras win) |

## Train (v1 lesson)

- MPS float16 + lr=2e-4 → **NaN adapter** (discard)
- Stable: `--lr 8e-5 --max-grad-norm 0.3` · then epoch 2
- Conflicting duplicate prompts in v0+v1 hurt clarify — builder now dedupes
- Next: retrain v1.1 on deduped 74 @ lr≈1.2e-4

## Smoke

```bash
# quality bar
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  ~/Projects/neurolab/config/sovereign.tiny-v0.toml   # :8091

# experiment
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  ~/Projects/neurolab/config/sovereign.tiny-v1.toml   # :8092
```
