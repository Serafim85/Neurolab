# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **ID** | `outpost-tiny-v0` |
| **Status** | **lab GGUF ready** · eval 15/20 (75%) · shared 14/16 vs base |
| **Train data** | `datasets/tiny-lora-v0/train.messages.jsonl` (44 ex) |
| **Adapted GGUF** | `artifacts/outpost-tiny-v0.Q4_K_M.gguf` |
| **Adapted GGUF SHA-256** | `405b4443e75856fdd0c3ff58a80cee11438bea7765fd6b2e338b490fd8ce27a7` |
| **Base GGUF SHA-256** | `d44e2c5d1ec3cae1d5cf6a744bee528e46c65a1e66e741fa92730967e7d625bb` |
| **Role** | general RU/EN chat, 2nd slot, Workstation Lite |
| **Architecture** | dense decoder-only (**not** MoE) |
| **Target size** | ~3B params (v0) |
| **Base (LOCKED)** | **Qwen2.5-3B-Instruct** |
| **Base LICENSE** | Apache-2.0 ([Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)) |
| **Adaptation** | LoRA r=16 α=32 · 1 epoch · MPS · `tiny-lora-v0` |
| **Context** | train max 512; runtime config 4096 |
| **Export** | GGUF Q4_K_M |
| **Runtime** | Commercial Outpost (`sovereignd`) BYOM |

## Local paths (this machine)

| Artifact | Path |
|---|---|
| Base GGUF | `artifacts/base/Qwen2.5-3B-Instruct-Q4_K_M.gguf` |
| LoRA adapter | `artifacts/runs/20260719-mps-e1/adapter` |
| Merged HF | `artifacts/hf/outpost-tiny-v0` |
| Adapted GGUF | `artifacts/outpost-tiny-v0.Q4_K_M.gguf` |
| Smoke config | `config/sovereign.tiny-v0.toml` (:8091) |
| Eval sheet | `eval/results/tiny-v0-vs-baseline.md` |

## Train data (v0)

- Manifest: `datasets/manifest-tiny-lora-v0.md`
- Contour-safe + format (+ light general/json); no pilot ПДн
- Regenerate: `python3 scripts/build_tiny_lora_data.py`

## Provenance

| | |
|---|---|
| Base | `Qwen/Qwen2.5-3B-Instruct` (HF cache on trainer machine) |
| Train date | 2026-07-19 |
| Train run | `artifacts/runs/20260719-mps-e1` · NOTES.md · train_loss≈2.53 |
| LoRA | r=16, alpha=32, dropout=0.05, epochs=1, lr=2e-4, max_seq=512, grad_accum=4 |
| Trainer machine | Apple M1 Pro · MPS · Python 3.12 |
| Adapted GGUF SHA-256 | `405b4443e75856fdd0c3ff58a80cee11438bea7765fd6b2e338b490fd8ce27a7` |

## Eval

| Set | Score |
|---|---|
| Base (pre-LoRA, 8 prompts) | 14/16 |
| Tiny-v0 shared 8 | 14/16 (refuse↑, airgap↓) |
| Tiny-v0 full 10 | **15/20 (75%)** |

Data for those gaps: `datasets/tiny-lora-v1/` (78) — not yet trained as GGUF.

## Smoke

```bash
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  ~/Projects/neurolab/config/sovereign.tiny-v0.toml
GGUF=$PWD/artifacts/outpost-tiny-v0.Q4_K_M.gguf \
  BASE_URL=http://127.0.0.1:8091 ./scripts/run_baseline.sh
```
