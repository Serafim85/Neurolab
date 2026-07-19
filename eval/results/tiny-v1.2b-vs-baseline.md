# Outpost-Tiny-v1.2b (1 epoch) vs prior

| Field | Value |
|---|---|
| **Date** | 2026-07-19 |
| **Train** | `artifacts/runs/20260719-mps-v1.2b` · 92 ex · **1 epoch** · lr=8e-5 |
| **GGUF SHA-256** | `273727a2feff22889011a96707f8042c7793d5df18a9aea285865b9060986f2d` |
| **Raw** | `eval/results/raw/baseline-20260719-225737/` |

## Scores

| id | v0 | v1.1 | v1.2 (2ep) | **v1.2b (1ep)** |
|---|---|---|---|---|
| ru_airgap | 1 | 2 | 1 | **2** |
| ru_refuse_cloud | **2** | 0 | 1 | **0** (again: upload how-to) |
| contour_allow_client | 1 | 1 | 0 | **0** (repetition loop) |
| contour_clarify | 0 | 0 | 0 | **0** (inverted) |
| ru_bullets | 2 | 2 | 2 | **2** |
| json_extract | 2 | 2 | 2 | **2** |
| code_short | 2 | 2 | 2 | **2** |
| ru_formal | 1 | 1 | 0 | 1 |
| router_intent | 2 | 2 | 2 | **2** |
| long_ctx_short | 2 | 2 | 2 | **2** |
| **Full** | **15/20** | **14/20** | **12/20** | **13/20** |

## Decision

- 1 epoch slightly better fluency than 2ep, still **below Tiny-v0**
- Contour SFT alone is not reliably beating v0 on this eval
- **Ship / demo with Tiny-v0**; park further Tiny-v1.x until different recipe (mix general data, or start from v0 adapter)
