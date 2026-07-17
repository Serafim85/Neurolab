# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **ID** | `outpost-tiny-v0` |
| **Status** | baseline **scored** 14/16 (87.5%) — not adapted yet |
| **Base GGUF SHA-256** | `d44e2c5d1ec3cae1d5cf6a744bee528e46c65a1e66e741fa92730967e7d625bb` |
| **Role** | general RU/EN chat, 2nd slot, Workstation Lite |
| **Architecture** | dense decoder-only (**not** MoE) |
| **Target size** | ~3B params (v0) |
| **Base (LOCKED)** | **Qwen2.5-3B-Instruct** |
| **Base GGUF** | `Qwen2.5-3B-Instruct-Q4_K_M.gguf` |
| **Base LICENSE** | Apache-2.0 ([Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)) |
| **HF GGUF source** | `lmstudio-community/Qwen2.5-3B-Instruct-GGUF` (same as Outpost preset `qwen2.5-3b-instruct-q4`) |
| **Adaptation** | none yet → later LoRA rank 8–16 or light SFT |
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

## Smoke in Outpost

```bash
# from neurolab — after GGUF exists
./scripts/run_baseline.sh
# or point Commercial sovereign.toml [models].path at the same GGUF
```
