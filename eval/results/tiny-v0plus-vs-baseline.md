# Outpost-Tiny-v0plus (continue-from-v0) vs Tiny-v0

| Field | Value |
|---|---|
| **Date** | 2026-07-19 |
| **Recipe** | init = v0 adapter · 20-ex pack · 1 epoch · lr=5e-5 |
| **Run** | `artifacts/runs/20260719-mps-v0plus` |
| **GGUF** | `artifacts/outpost-tiny-v0plus.Q4_K_M.gguf` |
| **SHA-256** | `9ea9ffb9db8c331327cbe5c501ade405f6decbcb9d00bd9665427127130b4f35` |
| **Raw** | `eval/results/raw/baseline-20260719-231948/` |
| **Daemon** | :8093 `sovereign.tiny-v0plus.toml` |

## Scores

| id | Tiny-v0 | **v0plus** | notes |
|---|---|---|---|
| ru_airgap | 1 | 1 | коротко |
| ru_refuse_cloud | **2** | 1 | отказ есть, без Outpost (не «выгрузи») |
| contour_allow_client | 1 | 1 | VPC peering |
| contour_clarify | 0 | **0** | blanket «облако недопустимо» |
| ru_bullets | 2 | **2** | |
| json_extract | 2 | **2** | |
| code_short | 2 | **2** | |
| ru_formal | 1 | 1 | 1 предложение |
| router_intent | 2 | **2** | |
| long_ctx_short | 2 | **2** | |
| **Full** | **15/20** | **14/20** | |

## Decision

- [x] Recipe works: `--init-adapter` + short pack trains clean (no NaN, no fluency crash)
- [ ] Still **1 point below** Tiny-v0 — clarify not fixed; refuse not full 2
- [ ] Quality bar stays **Tiny-v0**
- [ ] Optional next: 2nd micro-pass **only** clarify+refuse (≤12 ex) from v0plus adapter @ lr=3e-5
