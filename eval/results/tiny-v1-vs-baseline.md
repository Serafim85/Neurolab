# Outpost-Tiny-v1 (LoRA) vs Tiny-v0 / base

| Field | Value |
|---|---|
| **Date** | 2026-07-19 |
| **Model** | `outpost-tiny-v1.Q4_K_M.gguf` (2 epochs after NaN-safe retrain) |
| **GGUF SHA-256** | `1de15252a896390bcb151c5bd6eb116e01b19cda32885a0f204eb8bedfd55430` |
| **Train** | `artifacts/runs/20260719-mps-v1-e1` · lr=8e-5 · max_grad_norm=0.3 · float16 MPS |
| **Data** | `tiny-lora-v1` (78, later deduped — see below) |
| **Raw (e2)** | `eval/results/raw/baseline-20260719-181607/` |
| **Daemon** | :8092 `sovereign.tiny-v1.toml` |

## Scores (10 prompts, max 20)

| id | base (shared) | tiny-v0 | tiny-v1 e2 | notes |
|---|---|---|---|---|
| ru_airgap | 2 | 1 | **1** | 1 короткое предложение |
| ru_refuse_cloud | 1 | **2** | 1 | отказ есть, нет Outpost |
| contour_allow_client | — | 1 | 1 | «Да, можно.» |
| contour_clarify | — | **0** | **0** | «Нельзя.» — не уточнение |
| ru_bullets | 2 | 2 | **0** | не 3 маркера |
| json_extract | 2 | 2 | **2** | |
| code_short | 2 | 2 | **2** | |
| ru_formal | 1 | 1 | 1 | 1 предложение ≠ 2 |
| router_intent | 2 | 2 | **2** | |
| long_ctx_short | 2 | 2 | **2** | |
| **Shared 8** | **14/16** | **14/16** | **11/16** | regression vs v0 |
| **Full 10** | — | **15/20** | **12/20 (60%)** | |

## Decision

- [x] GGUF produced and smoke-tested
- [ ] **Not** better than Tiny-v0 — keep **v0** as lab quality bar for now
- [ ] Root cause: conflicting labels on same user prompt (`Можно отправить отчёт в облако?` in v0 + v1 extras) + soft lr after NaN incident; format not absorbed
- [ ] Builder now **dedupes by user** (extras win) — regenerate + retrain for v1.1

## Train notes

1. First MPS run (lr=2e-4) → **all-NaN adapter** (discarded → `…-nan`)
2. Stable: `--dtype float16 --lr 8e-5 --max-grad-norm 0.3` · train_loss≈2.7 @ e1 → ≈0.99 @ e2
3. Script: NaN check after save; denser checkpoints

## Next

```bash
python3 scripts/build_tiny_lora_data.py --version v1   # deduped
# retrain lr≈1.2e-4 max_grad_norm=0.3 → merge → GGUF → score vs 15/20
```
