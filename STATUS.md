# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-19

---

## Summary

| Area | State |
|---|---|
| **Quality bar (use this)** | Tiny-v0 GGUF · **15/20** |
| Tiny-v1.2b (1ep) | **13/20** — лучше 2ep, хуже v0 |
| Contour-only SFT ladder | paused — not beating v0 |

### What «quality bar = Tiny-v0» means

Для smoke/demo/пилота указываем в конфиге **`outpost-tiny-v0.Q4_K_M.gguf`**.  
Файлы `outpost-tiny-v1*.gguf` — лабораторные эксперименты; пока score ниже — не заменяют v0.

---

## Backlog

1. New recipe before more Tiny-v1: mix general chat **or** continue from v0 adapter  
2. Construct S1 validate  
3. Suite `extract`  
4. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-19 | v1.2b 1-epoch · 13/20 · SHA `273727a2…` |
| 2026-07-19 | v1.2 2ep 12/20 · v1.1 14/20 · v0 **15/20** |

---

## Session log

### 2026-07-19 — v1.2b + clarify «quality bar»

- 1 epoch on 92 → **13/20**; refuse again wrong.
- Explained: quality bar = which GGUF we treat as best for real use (still v0).
