# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-19

---

## Summary

| Area | State |
|---|---|
| Docs / Construct / Canon / Contour | ✅ |
| tiny-lora-v0 data (44) | ✅ |
| Train → GGUF on this Mac | ✅ `outpost-tiny-v0.Q4_K_M.gguf` |
| Eval sheet | ✅ **15/20** · `eval/results/tiny-v0-vs-baseline.md` |
| CARD provenance | ✅ |
| Tiny-v1 data | backlog |

---

## In progress

| Item | Notes |
|---|---|
| — | resume pack closed; next = Tiny-v1 data when human asks |

---

## Backlog

1. Tiny-v1 data: contour_clarify, formal×2, richer airgap, allow_client detail  
2. Retrain / 2nd epoch → re-eval  
3. Construct S1 validate script  
4. Suite `extract` specialist  
5. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-18…19 | Lab docs, Construct, Canon, Contour, Advisor planned |
| 2026-07-18 | Baseline base 3B 14/16 · tiny-lora-v0 dataset |
| 2026-07-19 | Train MPS e1 → merge → Q4 GGUF · smoke :8091 |
| 2026-07-19 | **Resume pack:** eval sheet, CARD, `run_baseline.sh` GGUF= override |

---

## Artifacts (local, not in git)

| Path | Notes |
|---|---|
| `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | ~1.8G · SHA `405b4443…ce27a7` |
| `artifacts/runs/20260719-mps-e1/adapter` | PEFT |
| `artifacts/hf/outpost-tiny-v0` | merged HF ~5.7G |

---

## Session log

### 2026-07-19 — Resume pack after pause

- **Done:** `eval/results/tiny-v0-vs-baseline.md` (15/20); CARD provenance; `run_baseline.sh` accepts `GGUF=` + works without local file if daemon up; STATUS cleared pause.
- **Verify:** `cat eval/results/tiny-v0-vs-baseline.md` · `cat models/outpost-tiny/CARD.md`
- **Next (human):** Tiny-v1 data round or stop.

### 2026-07-19 — PAUSE (historical)

- Train/merge/GGUF/smoke done; internet drop; resumed above.
