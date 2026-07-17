# Neurolab STATUS

**Last updated:** 2026-07-18

## In progress

| Item | Notes |
|---|---|
| Bootstrap | repo skeleton + Tiny CARD + Micro-MoE plan |
| Decide track priority | Tiny-first **or** one specialist (extract) + router stub |

## Backlog

1. Baseline eval scores on Qwen2.5-1.5B/3B (Commercial Outpost)
2. Outpost-Tiny-v0 LoRA smoke → GGUF
3. Suite: `extract` specialist v0 (JSON/fields) — first micro-MoE expert
4. Suite: `router` (classify → expert id) — can start as rules, then small LM
5. `summarize` RU polish specialist
6. Embedding pack (align with Commercial Phase 2)

## Done

| Date | Item |
|---|---|
| 2026-07-18 | Repo created; STRATEGY + MICRO-MOE + Tiny CARD + eval prompts |

## Blockers

- GPU / Colab access for first LoRA (optional: CPU LoRA on tiny base — slow)
