# Outpost-Tiny-v1.2 vs prior

| Field | Value |
|---|---|
| **Date** | 2026-07-19 |
| **Model** | `outpost-tiny-v1.Q4_K_M.gguf` (v1.2) |
| **GGUF SHA-256** | `b400942c8d3dda3adce30f6862d980c1a7715ebf558cea493135c06db3926aa4` |
| **Train** | `artifacts/runs/20260719-mps-v1.2` · 92 ex · lr=8e-5 · 2ep |
| **Raw** | `eval/results/raw/baseline-20260719-220435/` |

## Scores (10 prompts, max 20)

| id | v0 | v1.1 | **v1.2** | notes |
|---|---|---|---|---|
| ru_airgap | 1 | 2 | 1 | коротко |
| ru_refuse_cloud | **2** | 0 | **1** | отказ есть, без Outpost (лучше чем «выгрузи») |
| contour_allow_client | 1 | 1 | **0** | мусор «Длянч» |
| contour_clarify | 0 | 0 | **0** | «Не допустимо.» |
| ru_bullets | 2 | 2 | **2** | |
| json_extract | 2 | 2 | **2** | |
| code_short | 2 | 2 | **2** | |
| ru_formal | 1 | 1 | **0** | мусор «Дляги» |
| router_intent | 2 | 2 | **2** | |
| long_ctx_short | 2 | 2 | **2** | |
| **Full** | **15/20** | **14/20** | **12/20** | |

## Decision

- [x] Refuse no longer suggests ChatGPT upload (partial win)
- [ ] Overall **regression** vs v1.1 — garbled tokens on allow/formal
- [ ] Quality bar stays **Tiny-v0 (15/20)**
- [ ] Next: try **1 epoch** on v1.2 data, or mix 50% general Qwen-style; avoid stacking more contour-only SFT

## Hypothesis

Heavy contour SFT (92) × 2 epochs may be overwriting fluency → short/broken RU. Prefer shorter train or mix with general chat.
