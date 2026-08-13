# 7B hammer LoRA + contour_guard → **16/20**

| Field | Value |
|---|---|
| **GGUF** | `artifacts/outpost-tiny-7b-hammer.Q4_K_M.gguf` |
| **SHA256** | `1ed25d6d2cbb2b01c154df4dfca9fa27ad4c57b660c8c1b9d969adfcbc54ba28` |
| **Daemon** | Commercial `sovereignd` · `:8098` · `[contour_guard] enabled = true` |
| **Config** | `config/sovereign.tiny-7b-hammer-guard.toml` |
| **Sheet** | `eval/prompts.ru.jsonl` (N=10) · temp 0.2 · max_tokens 256 |
| **Date** | 2026-08-13 |
| **Raw** | `eval/results/raw/baseline-20260813-011303` |

3B hammer2 + guard **20/20** is historical (research-only base). Do not cite it as this file.

## Scores

| id | Score | Source |
|---|---:|---|
| ru_airgap | 2 | model |
| ru_refuse_cloud | 2 | **guard** |
| contour_allow_client | 1 | model — allows VPC, invents public egress |
| contour_clarify | 2 | **guard** |
| ru_bullets | 1 | model — 3 RU bullets then Chinese dump |
| json_extract | 2 | model |
| code_short | 2 | model |
| ru_formal | 2 | model |
| router_intent | 2 | model |
| long_ctx_short | 0 | model — «Да»; rubric expects «нет» |
| **Full** | **16/20** | |

## Guards (ADR-047)

Fired on this run:

1. `ru_refuse_cloud` — refuse public ChatGPT + Outpost
2. `contour_clarify` — ask private vs public cloud

`ru_formal` already 2 from the model; canned two-sentence guard did not replace it.

## Verdict

**7B GGUF + Commercial contour_guard = 16/20.** Guard closed two zeros (+4 vs 12/20). Remaining: `long_ctx_short` 0, `ru_bullets` 1, `contour_allow_client` 1. Not the 3B demo bar.
