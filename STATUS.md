# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-19

---

## Summary

| Area | State |
|---|---|
| Tiny-v0 GGUF | ✅ **15/20** — **quality bar** |
| Tiny-v1.1 | 14/20 |
| Tiny-v1.2 data+GGUF | ✅ train ok · eval **12/20** (refuse↑, fluency↓) |

---

## In progress

| Item | Notes |
|---|---|
| — | |

---

## Backlog

1. Tiny-v1.2b: **1 epoch** on same 92 (less overwrite) OR mix general chat  
2. Construct S1 validate  
3. Suite `extract`  
4. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-19 | **v1.2** data 92 + train + GGUF · eval 12/20 |
| 2026-07-19 | v1.1 14/20 · NanGuard · v0 15/20 |

---

## Artifacts (local)

| Path | Score |
|---|---|
| `outpost-tiny-v0.Q4_K_M.gguf` | **15/20** use |
| `outpost-tiny-v1.Q4_K_M.gguf` | 12/20 (v1.2 SHA `b400942c…`) |

---

## Session log

### 2026-07-19 — Tiny-v1.2

- Data: refuse hard + clarify/formal → 92 · `datasets/tiny-lora-v1.2/`
- Train: lr8e-5 × 2ep · NaN=0 · SHA `b400942c…6aa4`
- Eval **12/20**: refuse better than v1.1, but allow/formal garbled.
- Next: 1-epoch retrain on same data if human wants.
