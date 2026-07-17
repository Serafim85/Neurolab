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

## Быстрый старт

1. Заполнить `models/outpost-tiny/CARD.md` (база + LICENSE)
2. Прогнать baseline: `eval/prompts.ru.jsonl` на чужом 1.5–3B в Outpost
3. Первый LoRA → GGUF → положить путь в `sovereign.toml` Commercial

Веса и датасеты в git **не** кладём (см. `.gitignore`).
