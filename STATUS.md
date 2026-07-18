# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-18

---

## Summary

| Area | State |
|---|---|
| Agent docs | ✅ AGENTS + architecture pack |
| **Construct** | ✅ schema v0.1 + `docs/CONSTRUCT.md` (NL-ADR-006) |
| **Canon** | ✅ `docs/INTELLECTUAL-CANON.md` (NL-ADR-007) |
| Tiny base | ✅ Qwen2.5-3B Q4 locked + pulled |
| Baseline | ✅ **14/16 (87.5%)** |
| LoRA | 🔜 data prep next |
| Micro-MoE | cards + construct slots (not trained) |
---

## In progress

| Item | Notes |
|---|---|
| **LoRA data prep** | gaps: refuse-cloud + format discipline (`GOALS.md` / baseline sheet) |

---

## Backlog

1. Tiny LoRA / light SFT → GGUF → re-eval vs 14/16
2. Construct S1: validate script for `construct/*.toml`
3. Suite `extract` specialist v0 → enable slot in construct
4. Construct pack layout (`packs/<id>/`)
5. Commercial S3–S5: load construct + profile autotune (Gate B+)
5b. **Construct Advisor** S6 (NL-ADR-008) — после S4; A1 rules first
6. `summarize` specialist
7. Embedding pack (align Commercial Phase 2)
8. Private git remote for neurolab (human)
---

## Done

| Date | Item |
|---|---|
| 2026-07-18 | Repo bootstrap + MICRO-MOE strategy |
| 2026-07-18 | Locked Tiny base; pull; baseline 14/16 |
| 2026-07-18 | **Full agent documentation pack** — AGENTS, ARCHITECTURE, GOALS, INTEGRATION, SCALE-PLAN, ENGINEERING, DECISIONS, INDEX, cursor rule |
| 2026-07-18 | **Model Construct (NL-ADR-006)** — `docs/CONSTRUCT.md` + `construct/example.toml`: слоты, router, hardware profiles, autotune v1 |
| 2026-07-18 | **Intellectual Canon (NL-ADR-007)** — книги, papers, Anthropic/OpenAI, future vectors → Outpost lineage |

---

## Blockers

- GPU / Colab for comfortable LoRA (CPU possible, slow)

---

## Session log

### 2026-07-18 — Construct Advisor (planned)

- **Idea:** маленький оценщик: intent пользователя × железо → propose construct (слоты/profile); Accept человеком.
- **ADR:** NL-ADR-008 · spec in `docs/CONSTRUCT.md` §7b · S6 after profiles work.
- **v0:** rules + skills + RAM cap; не тяжёлый агент и не silent swap.
- **Does not block:** Tiny LoRA.

### 2026-07-18 — Intellectual Canon

- **Goal:** мощная будущая база линейки — книги, статьи, практики frontier labs.
- **Done:** `docs/INTELLECTUAL-CANON.md` + NL-ADR-007; столпы dense/scaling/post-train/Construct/interpretability; reading order.
- **Filter:** Contour + Measure + Construct; не клонировать GPT-кластеры.
- **Next:** LoRA data prep (canon: LoRA + InstructGPT + Qwen2.5 post-train).

### 2026-07-18 — Model Construct foundation

- **Goal:** заложить гибкость, настраиваемость, масштаб, автоподстройку к железу.
- **Done:** `docs/CONSTRUCT.md`, `construct/example.toml`, NL-ADR-006; updates ARCHITECTURE/SCALE/INTEGRATION/AGENTS.
- **Idea:** эволюция = слоты в манифесте + profiles (lite→dc), не одна жёсткая сеть; autotune = выбор профиля по RAM, lock after boot.
- **Next:** LoRA data prep; optional construct validate script (S1).

### 2026-07-18 — Agent documentation + architecture pack

- **Goal:** полная документация для агентов; архитектура сети; цели; встраивание; scale; инженерный подход.
- **Done:** `AGENTS.md`, `docs/{INDEX,ARCHITECTURE,GOALS,INTEGRATION,SCALE-PLAN,ENGINEERING,DECISIONS}.md`, `.cursor/rules/00-neurolab.mdc`, README hub.
- **Doctrine:** reliability & quality; min resources → max measured result (`NL-ADR-004`).
- **Verify:** open `docs/INDEX.md`; agents start at `AGENTS.md`.
- **Next:** LoRA data prep for Tiny (refuse + format).

### 2026-07-18 — Tiny baseline

- Base Qwen2.5-3B-Instruct Q4; SHA `d44e2c5d…`; scores 14/16.
- Raw: `eval/results/raw/baseline-20260718-024355/`.
