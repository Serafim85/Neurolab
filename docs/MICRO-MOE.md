# Micro-MoE — suite мини-нейронок

## Идея

Не одна Mixture-of-Experts архитектура, а **несколько маленьких специалистов + маршрутизатор**:

```text
запрос → router → {extract | summarize | chat-tiny | …} → ответ
```

Это и есть «микро-MoE» для Outpost: эксперты = отдельные GGUF (или LoRA), роутинг = правила / маленький LM / agent pipeline.

## Есть ли перспектива?

**Да — высокая**, особенно для вашего продукта.

| Плюс | Почему для Outpost |
|---|---|
| RAM / CPU | на филиале держим 1–2 маленьких, не 70B |
| Качество на узком | extract JSON часто лучше маленького specialist, чем «общий» 3B |
| Совпадает с runtime | ADR-031 multi-model / agent stages уже про это |
| Гос / ИБ | каждый pack с отдельным паспортом; проще экспертиза |
| Итерации | дообучить одного эксперта дешевле, чем весь monolith |
| Монетизация | industry packs = набор экспертов под vertical |

| Минус / риск | Как закрыть |
|---|---|
| Сложность ops | сначала **последовательный** swap (как Gate B), не 5 моделей в RAM |
| Плохой router | v0 = правила / keywords; LM-router — после 2 экспертов |
| «Слабый chat» | suite **не заменяет** Mid; chat остаётся Tiny/Mid |
| Размытие фокуса | максимум **один** новый эксперт за итерацию |

## Когда suite лучше одного Tiny

- Агентские пайплайны (classify → extract → write)
- Жёсткий JSON / поля документов
- Разные verticals (analytics vs secretariat) без одной «жирной» сети
- Слабое железо: несколько 0.5–1.5B по очереди

## Когда хватает одного Tiny

- Демо «просто поговори»
- Workstation Lite / один слот
- Пока нет данных под узких экспертов

## Целевой suite v0 (не всё сразу)

| ID | Размер (ориентир) | Роль | Старт |
|---|---|---|---|
| `router` | rules → потом ≤1.5B | выбрать эксперта | stub rules |
| `extract` | 1.5–3B LoRA | JSON / поля / CSV hints | **первый эксперт** |
| `summarize` | 1.5–3B LoRA | RU bullets / minutes-style | после extract |
| `chat` | = Outpost-Tiny | общий диалог | Track A |
| `embed` | отдельная embed-модель | RAG | Phase 2 Commercial |

**Не в v0:** arch-MoE (Mixtral-style), vision specialist (есть BYOM vision в runtime), 7B+ эксперты.

## Связь с Commercial

- Роутинг в проде → `agents.toml` / ModelPool (Gate B), не отдельный Python-сервис в пилоте.
- Neurolab варит веса; Outpost исполняет.
