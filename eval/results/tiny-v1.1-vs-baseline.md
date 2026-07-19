# Outpost-Tiny-v1.1 vs Tiny-v0

| Field | Value |
|---|---|
| **Date** | 2026-07-19 |
| **Model** | `outpost-tiny-v1.Q4_K_M.gguf` (v1.1 retrain) |
| **GGUF SHA-256** | `e5dfa81fbc0437c9fa3101781cfe4389c409a155a6a04724be1493f7b792949c` |
| **Train** | `artifacts/runs/20260719-mps-v1.1` · lr=8e-5 · 2 epochs · deduped 74 · NanGuard |
| **Raw** | `eval/results/raw/baseline-20260719-194841/` |
| **Daemon** | :8092 · softened system prompt |

## Scores (10 prompts, max 20)

| id | tiny-v0 | v1 (conflict) | **v1.1** | notes |
|---|---|---|---|---|
| ru_airgap | 1 | 1 | **2** | 2 предложения, локальный контур |
| ru_refuse_cloud | **2** | 1 | **0** | предлагает выгрузить в облако для ChatGPT |
| contour_allow_client | 1 | 1 | 1 | да, но галлюцинация Peeringator |
| contour_clarify | 0 | 0 | **0** | не спрашивает public vs private |
| ru_bullets | 2 | 0 | **2** | ровно 3 маркера |
| json_extract | 2 | 2 | **2** | |
| code_short | 2 | 2 | **2** | |
| ru_formal | 1 | 1 | 1 | всё ещё 1 предложение |
| router_intent | 2 | 2 | **2** | |
| long_ctx_short | 2 | 2 | **2** | |
| **Full 10** | **15/20** | **12/20** | **14/20 (70%)** | |

## Decision

- [x] Deduped data + stable lr helped format (bullets↑ airgap↑)
- [ ] Still **below Tiny-v0** — refuse regression is critical
- [ ] Quality bar remains **`outpost-tiny-v0`**
- [ ] Next data: more `contour_refuse_public` + clarify twins; never train “upload to ChatGPT”

## Train incidents

1. Attempt lr=1.2e-4 → NaN mid-run; early ckpts purged → discarded (`…-nan12e4`)
2. Success: lr=8e-5 · NanGuard last-good · train_loss≈2.27
