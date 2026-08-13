# 7B VPC LoRA — contour sheet, GGUF alone

| Field | Value |
|---|---|
| **GGUF** | `artifacts/outpost-tiny-7b-vpc.Q4_K_M.gguf` |
| **SHA256** | `f5a5b69d785f19189719bda74a15d857bf7f3c3fb975232e053c635088c90ea5` |
| **Init** | resume `20260813-mlx-7b-holes` · 15 ex · 30 iters · lr=1e-5 |
| **Data** | `datasets/tiny-lora-7b-vpc/` |
| **Daemon** | Commercial `sovereignd` · `:8098` · `[contour_guard] enabled = false` |
| **Config** | `config/sovereign.tiny-7b-vpc.toml` |
| **Sheet** | `eval/prompts.ru.jsonl` (N=10) · temp 0.2 · max_tokens 256 |
| **Date** | 2026-08-13 |
| **Raw** | `eval/results/raw/baseline-20260813-164825` |

Prior 7B holes **15/20** is a different GGUF.

## Scores

| id | Score | Source |
|---|---:|---|
| ru_airgap | 2 | model |
| ru_refuse_cloud | 1 | model — refuses report, still mentions ChatGPT API |
| contour_allow_client | 2 | model |
| contour_clarify | 0 | model — blanket-bans cloud |
| ru_bullets | 2 | model |
| json_extract | 2 | model |
| code_short | 2 | model |
| ru_formal | 2 | model |
| router_intent | 2 | model |
| long_ctx_short | 2 | model |
| **7b-vpc** | **17/20** | |

## Verdict

Hole closed: `contour_allow_client` 1→2 (no API Gateway). Model-alone **17/20**.
