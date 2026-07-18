# Dataset manifest — Outpost-Tiny LoRA v0

| Field | Value |
|---|---|
| **ID** | `tiny-lora-v0` |
| **Purpose** | Contour-safe + format discipline (close baseline gaps) |
| **Policy** | `docs/CONTOUR-EGRESS.md` · NL-ADR-009 |
| **Base model** | Qwen2.5-3B-Instruct |
| **PII** | none — synthetic only |
| **LICENSE of this set** | CC0-equivalent synthetic (Outpost Neurolab) |
| **Upstream base LICENSE** | Apache-2.0 (Qwen) — unchanged |

## Files

| Path | Role |
|---|---|
| `tiny-lora-v0/train.messages.jsonl` | Chat messages for SFT/LoRA |
| `tiny-lora-v0/STATS.md` | counts by tag |
| `../scripts/build_tiny_lora_data.py` | regenerates JSONL |

## Mix

| Tag | Focus |
|---|---|
| `contour_refuse_public` | no ChatGPT/Claude/public SaaS for internal data |
| `contour_allow_client` | private/own cloud OK |
| `contour_clarify` | ask which contour |
| `format_bullets` | exactly N markers |
| `format_sentences` | exactly N sentences |
| `format_short` | one word |
| `general_ru` | air-gap / Outpost — anti-forget |
| `json_code` | light JSON/code/router labels |

## Regenerate

```bash
python3 scripts/build_tiny_lora_data.py
```

## Train hint (next)

```text
data: datasets/tiny-lora-v0/train.messages.jsonl
base: Qwen/Qwen2.5-3B-Instruct
lora_rank: 16 · epochs: 1–2 · lr: ~2e-4
export → merge → GGUF Q4 → artifacts/outpost-tiny-v0.Q4_K_M.gguf
re-eval: ./scripts/run_baseline.sh vs 14/16
```
