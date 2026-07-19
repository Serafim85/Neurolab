# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-19

---

## Summary

| Area | State |
|---|---|
| Tiny-v0 GGUF | ✅ **15/20** — **quality bar** |
| Tiny-v1.1 GGUF | ✅ **14/20** — лучше 12, хуже v0 (refuse↓) |
| NanGuard in train | ✅ last-good + stop on NaN |

---

## In progress

| Item | Notes |
|---|---|
| — | |

---

## Backlog

1. Tiny-v1.2 data: reinforce refuse ChatGPT; clarify public vs private; formal×2  
2. Construct S1 validate  
3. Suite `extract`  
4. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-19 | Tiny-v1.1: deduped 74 · lr8e-5 · 2ep · GGUF · **14/20** |
| 2026-07-19 | train NanGuard / save_total_limit=40 |
| 2026-07-19 | Tiny-v0 15/20 · Tiny-v1 conflict 12/20 |

---

## Artifacts (local)

| Path | Score | Notes |
|---|---|---|
| `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | **15/20** | use this |
| `artifacts/outpost-tiny-v1.Q4_K_M.gguf` | 14/20 | SHA `e5dfa81f…949c` · v1.1 |
| `artifacts/runs/20260719-mps-v1.1/` | | adapter + last-good |

---

## Session log

### 2026-07-19 — Tiny-v1.1 retrain

- lr=1.2e-4 NaN discarded; stable **8e-5 × 2 epochs** on deduped 74 + NanGuard.
- Eval **14/20** (bullets/airgap↑, refuse catastrophic↓). Bar stays v0.
- Verify: `cat eval/results/tiny-v1.1-vs-baseline.md`
