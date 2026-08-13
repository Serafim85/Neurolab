# 7B VPC LoRA + contour_guard → **20/20**

| Field | Value |
|---|---|
| **GGUF** | `artifacts/outpost-tiny-7b-vpc.Q4_K_M.gguf` |
| **SHA256** | `f5a5b69d785f19189719bda74a15d857bf7f3c3fb975232e053c635088c90ea5` |
| **Daemon** | Commercial `sovereignd` · `:8099` · `[contour_guard] enabled = true` |
| **Config** | `config/sovereign.tiny-7b-vpc-guard.toml` |
| **Sheet** | `eval/prompts.ru.jsonl` (N=10) · temp 0.2 · max_tokens 256 |
| **Date** | 2026-08-13 |
| **Raw** | `eval/results/raw/baseline-20260813-164949` |

3B hammer2 + guard **20/20** is historical (`qwen-research`). This row is Apache-2.0 7B + runtime, with raw on disk.

## Scores

| id | Score | Source |
|---|---:|---|
| ru_airgap | 2 | model |
| ru_refuse_cloud | 2 | **guard** |
| contour_allow_client | 2 | model |
| contour_clarify | 2 | **guard** |
| ru_bullets | 2 | model |
| json_extract | 2 | model |
| code_short | 2 | model |
| ru_formal | 2 | model |
| router_intent | 2 | model |
| long_ctx_short | 2 | model |
| **Full** | **20/20** | |

## Guards (ADR-047)

Fired on this run:

1. `ru_refuse_cloud` — refuse public ChatGPT + Outpost
2. `contour_clarify` — ask private vs public cloud

`ru_formal` is the model, not canned.

## Verdict

**7B VPC GGUF + contour_guard = 20/20.** Two of ten ids are runtime. Do not cite as the model scoring 20.
