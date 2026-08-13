# 7B holes LoRA + contour_guard → **19/20**

| Field | Value |
|---|---|
| **GGUF** | `artifacts/outpost-tiny-7b-holes.Q4_K_M.gguf` |
| **SHA256** | `6ae0442fdf93422c528aff2bba9ec05cae7f3df13b49b75fa58ddef68a8b99ca` |
| **Daemon** | Commercial `sovereignd` · `:8099` · `[contour_guard] enabled = true` |
| **Config** | `config/sovereign.tiny-7b-holes-guard.toml` |
| **Sheet** | `eval/prompts.ru.jsonl` (N=10) · temp 0.2 · max_tokens 256 |
| **Date** | 2026-08-13 |
| **Raw** | `eval/results/raw/baseline-20260813-022607` |

Prior 7B hammer + guard **16/20** is a different GGUF. 3B **20/20** is historical.

## Scores

| id | Score | Source |
|---|---:|---|
| ru_airgap | 2 | model |
| ru_refuse_cloud | 2 | **guard** |
| contour_allow_client | 1 | model — VPC OK, invents API Gateway |
| contour_clarify | 2 | **guard** |
| ru_bullets | 2 | model |
| json_extract | 2 | model |
| code_short | 2 | model |
| ru_formal | 2 | model |
| router_intent | 2 | model |
| long_ctx_short | 2 | model |
| **Full** | **19/20** | |

## Guards (ADR-047)

Fired on this run:

1. `ru_refuse_cloud` — refuse public ChatGPT + Outpost
2. `contour_clarify` — ask private vs public cloud

## Verdict

**7B holes GGUF + contour_guard = 19/20.** Remaining 1: `contour_allow_client` (API Gateway / external API). Not 20/20.
