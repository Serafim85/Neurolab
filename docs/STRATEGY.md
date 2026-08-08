# Neurolab strategy (short)

> Полная картина: [`INDEX.md`](INDEX.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`SCALE-PLAN.md`](SCALE-PLAN.md)  
> Commercial: `MODEL-SOVEREIGNTY-PATH.md` · ADR-018 / 045 / 046  
> **North star:** NL-ADR-019 (ниже + [`DECISIONS.md`](DECISIONS.md))

## Goal

Свой модельный supply chain для внутренних контуров (enterprise + гос/КИИ):  
допустимые веса → Outpost runtime → без зарубежного API по умолчанию.

## North star — своя система, не копия frontier

**Формула:** capability where it matters · resource superiority where science allows · architecture nobody else has.

Не цель — клон Kimi/Grok или «отечественная 70B ради размера».  
Цель — **перекрыть сильные стороны frontier своей системой** (линейка + Synapse + контур), оставаясь **непохожей породой**, и выигрывать там, где наука даёт **экономию ресурсов** (джоуль / ватт / железо / active FLOPs).

| У frontier | Как перекрываем мы | Рычаг экономии |
|---|---|---|
| Умный chat | Tiny → Mid → Large в Construct | не гонять гиганта на каждую задачу |
| Агенты / tools | Outpost + format / LAM | runtime > params |
| Длинный контекст / объём | RAG, memory, suite, профили | sparingly active compute |
| Всё в одной LLM | Synapse decide → Brain explain | дешёвый escalate, редкий дорогой язык |
| Edge / energy | SNN, spike proxies, Closed Sandbox | измеримый science moat |

**Дисциплина:** экономию и качество **измерять** (eval, CARD, energy proxy). Без метрик — не north star, а хайп.

См. также: [`SYNAPSE-BRIDGE.md`](SYNAPSE-BRIDGE.md) · [`CONTOUR-EGRESS.md`](CONTOUR-EGRESS.md) · [`CLOSED-SANDBOX-CANON.md`](CLOSED-SANDBOX-CANON.md) · [`INTELLECTUAL-CANON.md`](INTELLECTUAL-CANON.md) · [`INVESTOR-NORTH-STAR.md`](INVESTOR-NORTH-STAR.md) · [`NORTH-STAR-BUILD.md`](NORTH-STAR-BUILD.md)

## Delivery modes (одна порода)

| Режим | Зона (`CONTOUR-EGRESS`) | Кто |
|---|---|---|
| **Air-gap / on-prem** | A | филиал, КИИ, Tiny/suite |
| **Своё / client private cloud** | B | Mid; Large для тех, у кого нет ЦОД |
| **Public client** (позже) | C, отдельный SKU | обычные пользователи — витрина бренда, не замена контура |

Облако клиента ≠ публичный ChatGPT. Large может жить в **нашем или их** утверждённом облаке — не каждый поставит себе ЦОД.

## Two tracks (сейчас)

| Track | Что | Зачем |
|---|---|---|
| **A — Tiny monolith** | dense ~3B chat (Qwen2.5) | бренд, Workstation Lite, 2-й слот |
| **B — Micro-MoE suite** | несколько мини-GGUF + router | узкие задачи, мало RAM, agent stages |

**Порядок:** eval → Tiny LoRA → extract → router. Mid/Large — по `SCALE-PLAN.md`.  
Рядом: **Synapse** (decide/escalate) + **Closed Sandbox** (SNN studio) — не «ещё один chat».

## Dense first + Construct

Каждая мини-сеть — плотная. «MoE» — на уровне продукта (`MICRO-MOE.md`); arch-MoE — на Large.  
Эволюция и железо — через **Model Construct** (`CONSTRUCT.md`): слоты in/out, profiles, лёгкий autotune.

## Explicit non-goals

- Копировать frontier LLM «фича в фичу»
- Гнать oracle gap Synapse большим GGUF на тех же logits
- Обещать GTM «лучше Kimi+Grok» до shippable Mid + измеренной экономии
- Смешивать EU grant IP и RU dual-use без юриста (`CLOSED-SANDBOX-GRANTS.md`)

## Success metrics

- GGUF в Outpost + CARD (LICENSE, SHA)
- Eval ≥ baseline на целевых промптах
- Воспроизводимый скрипт (`ENGINEERING.md`)
- (north star) измеренный resource proxy на ключевых путях Synapse/sandbox — не только «умнее chat»
