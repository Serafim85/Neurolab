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
| **tiny-lora-v1 data (78)** | ✅ clarify / formal×2 / richer airgap |
| Train → GGUF Tiny-v0 | ✅ eval **15/20** |
| Train Tiny-v1 → GGUF | backlog |

---

## In progress

| Item | Notes |
|---|---|
| — | data v1 ready; next = train when human asks |

---

## Backlog

1. Train Tiny-v1 LoRA → merge → GGUF → re-eval vs 15/20  
2. Construct S1 validate script  
3. Suite `extract` specialist  
4. Private git remote (human)

---

## Done

| Date | Item |
|---|---|
| 2026-07-18…19 | Lab docs, Construct, Canon, Contour |
| 2026-07-18 | Baseline base 3B 14/16 · tiny-lora-v0 |
| 2026-07-19 | Tiny-v0 train/merge/GGUF · resume pack 15/20 |
| 2026-07-19 | **tiny-lora-v1** (78) — builder `--version v1` |

---

## Artifacts (local, not in git)

| Path | Notes |
|---|---|
| `artifacts/outpost-tiny-v0.Q4_K_M.gguf` | ~1.8G · SHA `405b4443…ce27a7` |
| `artifacts/runs/20260719-mps-e1/adapter` | PEFT v0 |
| `artifacts/hf/outpost-tiny-v0` | merged HF |

---

## Session log

### 2026-07-19 — Tiny-v1 data

- **Done:** `datasets/tiny-lora-v1/` (78 = v0+34 extras); `manifest-tiny-lora-v1.md`; builder `--version v0|v1|all` + validate; train default data → v1.
- **Focus:** `contour_clarify` 14 · `format_sentences` 15 · `general_ru` airgap 13 · allow_client detail.
- **Verify:** `python3 scripts/build_tiny_lora_data.py --version v1` · `cat datasets/tiny-lora-v1/STATS.md`
- **Next:** train on Mac (same MPS flags as v0) when ready.
