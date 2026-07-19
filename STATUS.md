# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-19

---

## Summary

| Area | State |
|---|---|
| tiny-lora-v0 / Tiny-v0 GGUF | ✅ **15/20** quality bar |
| tiny-lora-v1 data | ✅ **74** (deduped) |
| Tiny-v1 train→GGUF | ✅ but eval **12/20** — not better than v0 |
| Tiny-v1.1 retrain | backlog (deduped data + lr≈1.2e-4) |

---

## In progress

| Item | Notes |
|---|---|
| — | pipeline closed; v1.1 when human asks |

---

## Backlog

1. Retrain Tiny-v1.1 on deduped 74 · lr≈1.2e-4 · max_grad_norm=0.3 → beat 15/20  
2. Soften system «Будь кратким» for format eval  
3. Construct S1 validate script  
4. Suite `extract` specialist  
5. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-19 | Tiny-v1 data + train (NaN salvage) + GGUF + eval 12/20 |
| 2026-07-19 | Builder dedupe-by-user; train NaN guard / grad clip |
| 2026-07-19 | Tiny-v0 resume pack 15/20 |

---

## Artifacts (local)

| Path | Notes |
|---|---|
| `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | **use this** · 15/20 |
| `artifacts/outpost-tiny-v1.Q4_K_M.gguf` | experiment · SHA `1de15252…` · 12/20 |
| `artifacts/runs/20260719-mps-v1-e1/` | adapter e2 · train_loss≈0.99 |

---

## Session log

### 2026-07-19 — Tiny-v1 train pipeline

- Train: first run NaN@lr2e-4; stable float16 lr8e-5 + grad clip; epoch 2 resume.
- GGUF Q4 · `config/sovereign.tiny-v1.toml` :8092 · eval **12/20** (worse than v0 15/20).
- Fix: dedupe conflicting user prompts in builder (74 ex).
- **Verify:** `cat eval/results/tiny-v1-vs-baseline.md`
- **Next:** v1.1 retrain on deduped set.
