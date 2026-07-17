# Outpost-Tiny — model card (draft)

| Field | Value |
|---|---|
| **ID** | `outpost-tiny-v0` |
| **Status** | draft — not trained yet |
| **Role** | general RU/EN chat, 2nd slot, Workstation Lite |
| **Architecture** | dense decoder-only (**not** MoE) |
| **Target size** | 1.5B–3B params |
| **Base (candidate)** | Qwen2.5-1.5B-Instruct **or** Qwen2.5-3B-Instruct |
| **Base LICENSE** | Apache-2.0 (verify on chosen HF revision) |
| **Adaptation** | LoRA (rank 8–16) or light SFT |
| **Context** | 4k–8k |
| **Export** | GGUF Q4_K_M |
| **Runtime** | Commercial Outpost (`sovereignd`) BYOM |

## Non-goals (v0)

- MoE layers, custom tokenizer, pretrain from scratch
- Pilot customer ПДн in training data
- Claiming “отечественная 70B” in GTM

## Train data (v0)

- Open instruct + synthetic RU (list paths in `datasets/` manifest later)
- Optional: short tool/JSON examples

## Eval

- See `../../eval/prompts.ru.jsonl`
- Pass bar: ≥70% not worse than base on same prompts (human or rubric)

## Provenance (fill after train)

| | |
|---|---|
| Base commit / HF revision | |
| Train date | |
| LoRA / checkpoint path (local) | |
| GGUF SHA-256 | |
| Trainer machine | |

## Smoke in Outpost

```bash
# Commercial repo — after GGUF exists
# sovereign.toml → model path = /path/to/outpost-tiny-v0.Q4_K_M.gguf
# sovereignd &
# sovereign chat -p "Кратко: что такое air-gap?"
```
