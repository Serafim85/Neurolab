# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **ID** | `outpost-tiny-v0` |
| **Status** | baseline 14/16 · **LoRA data ready** (`tiny-lora-v0`, 44 ex) — not trained yet |
| **Train data** | `datasets/tiny-lora-v0/train.messages.jsonl` |
| **Base GGUF SHA-256** | `d44e2c5d1ec3cae1d5cf6a744bee528e46c65a1e66e741fa92730967e7d625bb` |
| **Role** | general RU/EN chat, 2nd slot, Workstation Lite |
| **Architecture** | dense decoder-only (**not** MoE) |
| **Target size** | ~3B params (v0) |
| **Base (LOCKED)** | **Qwen2.5-3B-Instruct** |
| **Base GGUF** | `Qwen2.5-3B-Instruct-Q4_K_M.gguf` |
| **Base LICENSE** | Apache-2.0 ([Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)) |
| **HF GGUF source** | `lmstudio-community/Qwen2.5-3B-Instruct-GGUF` (same as Outpost preset `qwen2.5-3b-instruct-q4`) |
| **Adaptation** | pending LoRA rank 8–16 on `tiny-lora-v0` |
| **Context** | 4k–8k for train; runtime up to base limit |
| **Export (after train)** | GGUF Q4_K_M |
| **Runtime** | Commercial Outpost (`sovereignd`) BYOM |

## Why 3B (not 1.5B) for v0

- Already a **curated Outpost pull preset** → one command to get weights.
- Better RU / instruct quality for a meaningful baseline before LoRA.
- Still in Tiny band (Workstation Lite / 2nd slot); 1.5B can be a later distill.

## Non-goals (v0)

- MoE layers, custom tokenizer, pretrain from scratch
- Pilot customer ПДн in training data
- Claiming “отечественная 70B” in GTM

## Local paths (this machine)

| Artifact | Path |
|---|---|
| Base GGUF | `../../artifacts/base/Qwen2.5-3B-Instruct-Q4_K_M.gguf` |
| Neurolab daemon cfg | `../../config/sovereign.baseline.toml` |
| Eval prompts | `../../eval/prompts.ru.jsonl` |
| Baseline results | `../../eval/results/baseline-qwen25-3b.md` |
| LoRA data | `../../datasets/tiny-lora-v0/train.messages.jsonl` |

## Train data (v0)

- Manifest: `datasets/manifest-tiny-lora-v0.md`
- Contour-safe + format (+ light general/json); no pilot ПДн
- Regenerate: `python3 scripts/build_tiny_lora_data.py`

## Eval

1. Pull / place base GGUF (see `datasets/base-qwen25-3b.md`).
2. `./scripts/run_baseline.sh` → fills `eval/results/raw/`.
3. Human score with `eval/RUBRIC.md` → `eval/results/baseline-qwen25-3b.md`.
4. After LoRA: same prompts; pass bar ≥70% not worse than this baseline.

## Provenance (fill after train)

| | |
|---|---|
| Base HF revision / file SHA-256 | |
| Train date | |
| LoRA / checkpoint path (local) | |
| Adapted GGUF SHA-256 | |
| Trainer machine | |

## Train / export

See **`docs/TRAIN-TINY-LORA.md`**.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-train.txt
python3 scripts/train_tiny_lora.py
python3 scripts/merge_tiny_lora.py --adapter artifacts/runs/<stamp>/adapter
# then llama.cpp convert + quantize → artifacts/outpost-tiny-v0.Q4_K_M.gguf
```

## Smoke in Outpost

```bash
# after GGUF exists — config/sovereign.tiny-v0.toml
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  ~/Projects/neurolab/config/sovereign.tiny-v0.toml
BASE_URL=http://127.0.0.1:8091 ./scripts/run_baseline.sh
```
