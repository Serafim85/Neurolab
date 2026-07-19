# Dataset manifest — Outpost-Tiny LoRA v1.2

| Field | Value |
|---|---|
| **ID** | `tiny-lora-v1.2` |
| **Purpose** | Fix Tiny-v1.1 refuse regression + clarify/formal |
| **Base** | v0 + v1 extras + v1.2 extras · **deduped by user** |
| **Policy** | `docs/CONTOUR-EGRESS.md` · NL-ADR-009 |
| **PII** | none — synthetic only |

## Why v1.2

Tiny-v1.1 scored **14/20**; `ru_refuse_cloud` became **0** (model suggested uploading to ChatGPT).

| Focus | Change |
|---|---|
| `contour_refuse_public` | hard ChatGPT refusal + Outpost; no upload how-to |
| `contour_clarify` | more public vs private asks |
| `format_sentences` | more exactly-2 formal |
| `contour_allow_client` | clean VPC allow (no fake names) |

## Regenerate / train

```bash
python3 scripts/build_tiny_lora_data.py --version v1.2
python3 scripts/train_tiny_lora.py \
  --data datasets/tiny-lora-v1.2/train.messages.jsonl \
  --epochs 2 --lr 8e-5 --max-grad-norm 0.3 --max-seq-len 512
```
