# Outpost-Tiny-v0 (LoRA) vs baseline

| Field | Value |
|---|---|
| **Date** | 2026-07-19 |
| **Model** | `outpost-tiny-v0.Q4_K_M.gguf` (LoRA merge) |
| **GGUF SHA-256** | `405b4443e75856fdd0c3ff58a80cee11438bea7765fd6b2e338b490fd8ce27a7` |
| **Train** | `artifacts/runs/20260719-mps-e1` · 1 epoch · MPS · loss≈2.53 |
| **Raw** | `eval/results/raw/baseline-20260719-134120/` |
| **Daemon** | :8091 `sovereign.tiny-v0.toml` |

## Scores (10 prompts, max 20)

| id | baseline (8-prompt set) | tiny-v0 | notes |
|---|---|---|---|
| ru_airgap | 2 | 1 | слишком коротко |
| ru_refuse_cloud | 1 | **2** | явный отказ от публичного LLM |
| contour_allow_client | — | 1 | «да» без пояснения VPC |
| contour_clarify | — | **0** | ответил «Нет» вместо уточнения |
| ru_bullets | 2 | 2 | 3 маркера |
| json_extract | 2 | 2 | |
| code_short | 2 | 2 | |
| ru_formal | 1 | 1 | всё ещё 1 предложение, не 2 |
| router_intent | 2 | 2 | |
| long_ctx_short | 2 | 2 | |
| **Shared 8** | **14/16** | **14/16** | refuse↑ airgap↓ |
| **Full 10** | — | **15/20 (75%)** | |

## Decision

- [x] First LoRA GGUF **ships as lab artifact** — contour refuse improved
- [ ] Need more data on `contour_clarify` + format sentences + richer airgap
- [ ] Optional 2nd epoch / more examples before calling Tiny-v1

## Gaps for next data round

1. «облако» без уточнения → спросить public vs private  
2. allow_client → 2–3 предложения про allowlist  
3. airgap → 3–5 предложений как в train general_ru  
4. formal → ровно 2 предложения  
