# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-18

---

## Summary

| Area | State |
|---|---|
| Agent docs | ✅ AGENTS + architecture pack |
| Tiny base | ✅ Qwen2.5-3B Q4 locked + pulled |
| Baseline | ✅ **14/16 (87.5%)** |
| LoRA | 🔜 data prep next |
| Micro-MoE | cards only (not trained) |

---

## In progress

| Item | Notes |
|---|---|
| **LoRA data prep** | gaps: refuse-cloud + format discipline (`GOALS.md` / baseline sheet) |

---

## Backlog

1. Tiny LoRA / light SFT → GGUF → re-eval vs 14/16
2. Suite `extract` specialist v0
3. Router rules stub for Commercial Gate B
4. `summarize` specialist
5. Embedding pack (align Commercial Phase 2)
6. Private git remote for neurolab (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-18 | Repo bootstrap + MICRO-MOE strategy |
| 2026-07-18 | Locked Tiny base; pull; baseline 14/16 |
| 2026-07-18 | **Full agent documentation pack** — AGENTS, ARCHITECTURE, GOALS, INTEGRATION, SCALE-PLAN, ENGINEERING, DECISIONS, INDEX, cursor rule |

---

## Blockers

- GPU / Colab for comfortable LoRA (CPU possible, slow)

---

## Session log

### 2026-07-18 — Agent documentation + architecture pack

- **Goal:** полная документация для агентов; архитектура сети; цели; встраивание; scale; инженерный подход.
- **Done:** `AGENTS.md`, `docs/{INDEX,ARCHITECTURE,GOALS,INTEGRATION,SCALE-PLAN,ENGINEERING,DECISIONS}.md`, `.cursor/rules/00-neurolab.mdc`, README hub.
- **Doctrine:** reliability & quality; min resources → max measured result (`NL-ADR-004`).
- **Verify:** open `docs/INDEX.md`; agents start at `AGENTS.md`.
- **Next:** LoRA data prep for Tiny (refuse + format).

### 2026-07-18 — Tiny baseline

- Base Qwen2.5-3B-Instruct Q4; SHA `d44e2c5d…`; scores 14/16.
- Raw: `eval/results/raw/baseline-20260718-024355/`.
