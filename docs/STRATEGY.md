# Neurolab strategy (short)

> Полная картина: [`INDEX.md`](INDEX.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`SCALE-PLAN.md`](SCALE-PLAN.md)  
> Commercial: `MODEL-SOVEREIGNTY-PATH.md` · ADR-018 / 045 / 046

## Goal

Свой модельный supply chain для внутренних контуров (enterprise + гос/КИИ):  
допустимые веса → Outpost runtime → без зарубежного API.

## Two tracks

| Track | Что | Зачем |
|---|---|---|
| **A — Tiny monolith** | dense ~3B chat (Qwen2.5) | бренд, Workstation Lite, 2-й слот |
| **B — Micro-MoE suite** | несколько мини-GGUF + router | узкие задачи, мало RAM, agent stages |

**Порядок:** eval → Tiny LoRA → extract → router. Mid/Large — по `SCALE-PLAN.md`.

## Dense first + Construct

Каждая мини-сеть — плотная. «MoE» — на уровне продукта (`MICRO-MOE.md`).  
Эволюция и железо — через **Model Construct** (`CONSTRUCT.md`): слоты in/out, profiles, лёгкий autotune.
## Success metrics

- GGUF в Outpost + CARD (LICENSE, SHA)
- Eval ≥ baseline на целевых промптах
- Воспроизводимый скрипт (`ENGINEERING.md`)
