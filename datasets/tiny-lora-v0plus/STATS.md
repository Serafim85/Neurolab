# tiny-lora-v0plus stats

Total examples: **20**

| tag | count |
|---|---|
| `contour_allow_client` | 1 |
| `contour_clarify` | 6 |
| `contour_refuse_public` | 8 |
| `format_bullets` | 1 |
| `format_sentences` | 1 |
| `format_short` | 1 |
| `general_ru` | 1 |
| `json_code` | 1 |

## Recipe

- Continue from **Tiny-v0 adapter** (not fresh LoRA on base)
- 1 epoch · lr ≤ 8e-5 · max_grad_norm 0.3
- Focus: refuse ChatGPT + clarify cloud; keep format anchors

File: `datasets/tiny-lora-v0plus/train.messages.jsonl`
