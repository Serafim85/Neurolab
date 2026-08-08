# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **Demo / eval bar** | **hammer2 + contour_guard · 20/20** (Commercial ADR-047) |
| **Best lab GGUF alone** | `outpost-tiny-hammer` · **17/20** |
| **Base** | Qwen2.5-3B-Instruct (locked) |
| **Pilot pack** | [`docs/PILOT-CONTOUR-CHAT.md`](../../docs/PILOT-CONTOUR-CHAT.md) |

## GGUF

| ID | Path | Score |
|---|---|---|
| **hammer2 (use)** | `artifacts/outpost-tiny-hammer.Q4_K_M.gguf` | **17/20** alone · **20/20** + guard |
| v0 | `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | 15/20 |
| v0plus | `artifacts/outpost-tiny-v0plus.Q4_K_M.gguf` | 14/20 |
| v1.x | `artifacts/outpost-tiny-v1.Q4_K_M.gguf` | ≤13 |
| agent (exp.) | `artifacts/outpost-tiny-agent.Q4_K_M.gguf` | agent-v0 **16/20** (flat; not promoted) |
| agent-hn (exp.) | `artifacts/outpost-tiny-agent-hn.Q4_K_M.gguf` | agent-v0 **17/20** (+1; best agent exp) |
| agent-pb (exp.) | `artifacts/outpost-tiny-agent-pb.Q4_K_M.gguf` | agent-v0 **16/20** (focus miss; not promoted) |
| agent-mix (exp.) | `artifacts/outpost-tiny-agent-mix.Q4_K_M.gguf` | agent-v0 **17/20** (plateau = hn; not promoted) |

**Agent runtime:** hn + Commercial `[agent_format]` v2 → agent-v0 **20/20** — `eval/results/agent-v0-runtime-format.md`.


Do **not** promote micro / diverse / agent for pilot.

## Recipe (v0plus)

```bash
python3 scripts/build_tiny_lora_v0plus.py
python3 scripts/train_tiny_lora.py \
  --init-adapter artifacts/runs/20260719-mps-e1/adapter \
  --data datasets/tiny-lora-v0plus/train.messages.jsonl \
  --epochs 1 --lr 5e-5 --max-grad-norm 0.3 --grad-accum 4
```

Pilot smoke: `config/sovereign.tiny-hammer.toml` (:8096) · see `docs/PILOT-CONTOUR-CHAT.md`  
Legacy v0plus smoke: `config/sovereign.tiny-v0plus.toml` (:8093)
