# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-19

---

## Summary

| Area | State |
|---|---|
| **Quality bar** | Tiny-v0 · **15/20** |
| Tiny-v0plus (new recipe) | **14/20** — лучше v1.x fluency; не обогнал v0 |
| `--init-adapter` | ✅ in `train_tiny_lora.py` |

### Quality bar

Для demo/пилот — **`outpost-tiny-v0.Q4_K_M.gguf`**.  
v0plus / v1.x — lab, пока score &lt; 15/20.

---

## Backlog

1. Optional micro-pass: only clarify+refuse ≤12 ex from v0plus @ lr=3e-5  
2. Or pause Tiny → Construct S1 / suite extract  
3. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-19 | **v0plus**: continue-from-v0 · 20 ex · 14/20 · SHA `9ea9ffb9…` |
| 2026-07-19 | v1.2b 13/20 · v0 **15/20** |

---

## Session log

### 2026-07-19 — Tiny-v0plus recipe

- Pack `tiny-lora-v0plus` (20) · train from v0 adapter · lr5e-5 · 1ep  
- GGUF `:8093` · eval **14/20** (refuse safer than v1.2b, clarify still 0)  
- Verify: `cat eval/results/tiny-v0plus-vs-baseline.md`
