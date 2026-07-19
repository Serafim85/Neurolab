# Dataset manifest — Outpost-Tiny LoRA v1

| Field | Value |
|---|---|
| **ID** | `tiny-lora-v1` |
| **Purpose** | Close Tiny-v0 eval gaps: clarify, formal×2, richer airgap |
| **Base** | `tiny-lora-v0` (44) **+** v1 extras |
| **Policy** | `docs/CONTOUR-EGRESS.md` · NL-ADR-009 |
| **Base model** | Qwen2.5-3B-Instruct |
| **PII** | none — synthetic only |
| **LICENSE of this set** | CC0-equivalent synthetic (Outpost Neurolab) |

## Why v1

Tiny-v0 GGUF scored **15/20**; weak spots from `eval/results/tiny-v0-vs-baseline.md`:

| Eval id | Issue | v1 fix |
|---|---|---|
| `contour_clarify` | bare «Нет» | many ambiguous «облако» → ask public vs private |
| `ru_formal` | 1 sentence instead of 2 | more exactly-2 formal paraphrases |
| `ru_airgap` | too short | richer 3–5 sentence air-gap answers |
| `contour_allow_client` | thin «да» | longer VPC/allowlist detail |

## Files

| Path | Role |
|---|---|
| `tiny-lora-v1/train.messages.jsonl` | Chat messages for SFT/LoRA |
| `tiny-lora-v1/STATS.md` | counts by tag |
| `../scripts/build_tiny_lora_data.py` | regenerates JSONL (`--version v1`) |

## Regenerate

```bash
python3 scripts/build_tiny_lora_data.py --version v1
# or both: --version all
```

## Train hint

```bash
python3 scripts/train_tiny_lora.py \
  --data datasets/tiny-lora-v1/train.messages.jsonl \
  --epochs 1 --grad-accum 4 --max-seq-len 512
# merge → GGUF → smoke :8091 → score vs 15/20
```
