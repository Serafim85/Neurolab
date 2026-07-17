# Neurolab strategy

> Linked: Commercial `docs/MODEL-SOVEREIGNTY-PATH.md` · ADR-018 / ADR-045 / ADR-046

## Goal

Свой модельный supply chain для внутренних контуров (enterprise + гос/КИИ):  
допустимые веса → Outpost runtime → без зарубежного API.

## Two tracks (оба валидны)

| Track | Что | Зачем |
|---|---|---|
| **A — Tiny monolith** | одна dense 1.5–3B chat | бренд, Workstation Lite, 2-й слот |
| **B — Micro-MoE suite** | несколько мини-GGUF + router | узкие задачи, мало RAM, agent stages |

**Рекомендация:** вести **оба**, но не параллелить обучение.  
Порядок: **eval harness → Tiny-v0 LoRA smoke → один specialist (extract) → router**.

Потом: Mid 7–14B (мощный «свой» ответ госу). Large/arch-MoE — позже.

## Dense first inside each card

Каждая мини-сеть — **плотная**. «MoE» — на уровне **продукта** (кто вызван), не Mixtral-слоёв в одном файле.

## Success metrics

- GGUF грузится в Commercial Outpost
- Eval ≥ baseline на целевых промптах трека
- CARD.md: LICENSE, base, SHA, provenance (язык для ИБ)
