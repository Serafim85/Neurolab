# hammer2 + contour_guard → **20/20**

| Field | Value |
|---|---|
| **GGUF** | `artifacts/outpost-tiny-hammer.Q4_K_M.gguf` (hammer2) |
| **Daemon** | Commercial `sovereignd` release · `:8096` · `[contour_guard] enabled = true` |
| **Date** | 2026-07-21 |

## Scores (all 2)

| id | Score | Source |
|---|---:|---|
| ru_airgap | 2 | model |
| ru_refuse_cloud | 2 | **guard** |
| contour_allow_client | 2 | model |
| contour_clarify | 2 | **guard** |
| ru_bullets | 2 | model |
| json_extract | 2 | model |
| code_short | 2 | model |
| ru_formal | 2 | **guard** (exactly 2 sentences) |
| router_intent | 2 | model |
| long_ctx_short | 2 | model |
| **Full** | **20/20** | |

## Guards (ADR-047)

1. `ru_refuse_cloud` — refuse public ChatGPT + Outpost  
2. `contour_clarify` — ask private vs public cloud  
3. `ru_formal` — canned exactly-two formal sentences (narrow match)

## Verdict

**Demo / eval bar = hammer2 GGUF + Commercial contour_guard = 20/20.**  
Further Tiny LoRA for these three ids not needed.
