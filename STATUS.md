# Neurolab STATUS

**Last updated:** 2026-07-18

## In progress

| Item | Notes |
|---|---|
| **LoRA data prep** | next after accepted baseline; focus refuse-cloud + format discipline |

## Backlog

1. Tiny LoRA / light SFT → GGUF → re-eval vs 14/16 baseline
2. Suite: `extract` specialist v0
3. Suite: `router` stub / small LM
4. `summarize` specialist
5. Embedding pack (Commercial Phase 2)

## Done

| Date | Item |
|---|---|
| 2026-07-18 | Repo bootstrap + MICRO-MOE |
| 2026-07-18 | Locked Tiny base **Qwen2.5-3B-Instruct Q4**; pulled GGUF (~1.8G) |
| 2026-07-18 | Baseline on Outpost :8090 — **14/16 (87.5%)** · `eval/results/baseline-qwen25-3b.md` |

## Notes

- Daemon may still run: `sovereignd …/config/sovereign.baseline.toml` on **8090**
- Stop: Ctrl+C in that terminal or `kill` the sovereignd pid
