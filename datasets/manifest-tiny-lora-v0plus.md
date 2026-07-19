# Dataset manifest — Tiny v0plus (continue-from-v0)

| Field | Value |
|---|---|
| **ID** | `tiny-lora-v0plus` |
| **Purpose** | Patch refuse/clarify **without** overwriting Tiny-v0 fluency |
| **Recipe** | init = Tiny-v0 adapter · short pack (~24) · **1 epoch** · lr ≤ 8e-5 |
| **Not** | full contour dump (v1.2 92) — that regressed |

## Mix

| Tag | Role |
|---|---|
| `contour_refuse_public` | hard ChatGPT refuse + Outpost |
| `contour_clarify` | public vs private |
| anchors | airgap, bullets×3, formal×2, allow VPC, short, json |

## Train

```bash
python3 scripts/build_tiny_lora_v0plus.py
python3 scripts/train_tiny_lora.py \
  --init-adapter artifacts/runs/20260719-mps-e1/adapter \
  --data datasets/tiny-lora-v0plus/train.messages.jsonl \
  --epochs 1 --lr 5e-5 --max-grad-norm 0.3 --max-seq-len 512 \
  --grad-accum 4 --out artifacts/runs/<stamp>-v0plus
```
