# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **Quality bar (use)** | `outpost-tiny-v0` · **15/20** |
| **Best lab continue** | `outpost-tiny-v0plus` · **14/20** |
| **Base** | Qwen2.5-3B-Instruct |

## GGUF

| ID | Path | Score |
|---|---|---|
| v0 | `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | **15/20** |
| v0plus | `artifacts/outpost-tiny-v0plus.Q4_K_M.gguf` | 14/20 |
| v1.x | `artifacts/outpost-tiny-v1.Q4_K_M.gguf` | ≤13 |

## Recipe (v0plus)

```bash
python3 scripts/build_tiny_lora_v0plus.py
python3 scripts/train_tiny_lora.py \
  --init-adapter artifacts/runs/20260719-mps-e1/adapter \
  --data datasets/tiny-lora-v0plus/train.messages.jsonl \
  --epochs 1 --lr 5e-5 --max-grad-norm 0.3 --grad-accum 4
```

Smoke: `config/sovereign.tiny-v0plus.toml` (:8093)
