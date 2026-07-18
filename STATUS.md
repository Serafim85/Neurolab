# Neurolab STATUS

> Agents: update at end of every session.  
> Start: `AGENTS.md` → this file → `docs/DECISIONS.md`

**Last updated:** 2026-07-18

---

## Summary

| Area | State |
|---|---|
| Agent docs | ✅ |
| Construct / Canon / Contour | ✅ |
| Tiny base + baseline | ✅ 14/16 (8 prompts) |
| **LoRA data** | ✅ `tiny-lora-v0` **44** synthetic examples |
| LoRA train | 🔜 next |
| Micro-MoE | cards only |

---

## In progress

| Item | Notes |
|---|---|
| **Tiny LoRA train** | data ready → PEFT/Unsloth on Qwen2.5-3B → GGUF → re-eval |

---

## Backlog

1. Run LoRA + export GGUF `outpost-tiny-v0` + score vs baseline (eval now 10 prompts / max 20)
2. Optional: grow dataset beyond 44 if underfit
3. Construct S1 validate script
4. Suite `extract` specialist
5. Commercial construct load / Advisor (later)
6. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-18 | Docs pack, Construct, Canon, Contour egress, Advisor planned |
| 2026-07-18 | Baseline Qwen2.5-3B 14/16 |
| 2026-07-18 | **tiny-lora-v0 data** — contour-safe + format · `build_tiny_lora_data.py` |

---

## Session log

### 2026-07-18 — Tiny LoRA data prep

- **Done:** `scripts/build_tiny_lora_data.py` → 44 examples · manifest · eval +2 contour prompts · CARD/STATUS.
- **Verify:** `python3 scripts/build_tiny_lora_data.py` · `cat datasets/tiny-lora-v0/STATS.md`
- **Canon:** LoRA + InstructGPT-style post-train · CONTOUR-EGRESS.
- **Next:** train LoRA → GGUF → `./scripts/run_baseline.sh`
