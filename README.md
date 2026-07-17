# Нейролаб (neurolab)

Внутренняя лаборатория **своих весов** для Outpost.

| | |
|---|---|
| **Commercial runtime** | `~/Projects/AI-Platform-Vision` |
| **Старый product Lab** | `~/Projects/sov-lab` (API/Workbench R&D) |
| **Эта lab** | модели: Tiny, suite мини-специалистов («микро-MoE»), eval, export GGUF |

Не продаём пилотам напрямую. Цель: train → GGUF → smoke в `sovereignd`.

Стратегия: [`docs/STRATEGY.md`](docs/STRATEGY.md) · Micro-MoE: [`docs/MICRO-MOE.md`](docs/MICRO-MOE.md)  
Канон в Commercial: `AI-Platform-Vision/docs/MODEL-SOVEREIGNTY-PATH.md` (ADR-045)

## Треки

1. **Outpost-Tiny** — одна плотная chat-модель 1.5–3B (`models/outpost-tiny/`)
2. **Micro-MoE suite** — несколько мини-сеток + роутер (`models/suite/`) — *не* одна MoE-архитектура

## Быстрый старт (Tiny baseline)

База **зафиксирована:** Qwen2.5-3B-Instruct Q4.

```bash
./scripts/pull_base.sh
# terminal 2 — Commercial binary + neurolab config (port 8090):
#   ~/Projects/AI-Platform-Vision/target/release/sovereignd \
#     ~/Projects/neurolab/config/sovereign.baseline.toml
./scripts/run_baseline.sh
# score → eval/results/baseline-qwen25-3b.md (RUBRIC.md)
```

Веса в git **не** кладём (см. `.gitignore`).