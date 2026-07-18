# Цели и задачи моделей Нейролаб

---

## 1. Продуктовая цель

Дать Outpost **свой (или суверенно поставляемый) модельный слой** для внутренних контуров:

- enterprise / банк / интегратор;
- гос / КИИ — где «иностранный API» и часто «чужой upstream без паспорта» не проходят.

Runtime уже решает offline inference. Лаба решает: **какие веса**, **какое поведение**, **какой паспорт**.

---

## 2. Цели по горизонтам

| Горизонт | Цель | KPI |
|---|---|---|
| **H0 Now** | Измеримый baseline Tiny; инженерный контур Lab | baseline scored; docs complete |
| **H1** | Outpost-Tiny-v1 (LoRA) лучше базы на целевых gap | eval ≥ baseline; gaps refuse/format закрыты |
| **H2** | 1–2 specialist suite в agent pipeline | extract JSON ≥ Tiny на extract-промптах |
| **H3** | Outpost-Mid для «мощного» ответа в контуре | 7–14B pack + sizing guide |
| **H4** | Large / опционально arch-MoE на ЦОД | только при бюджете и спросе |

---

## 3. Задачи, которые модели **уже / скоро** решают

### 3.1 Outpost-Tiny (Track A) — общий локальный ассистент

| Задача | Сейчас (base 3B) | Цель после LoRA |
|---|---|---|
| RU объяснения (air-gap, offline AI) | ✅ baseline | стабильный тон «контур / ИБ» |
| Короткий код (утилиты, path checks) | ✅ | без воды |
| Структурированный JSON extract | ✅ | жёстче schema |
| Отказ слать секреты/отчёты в облако | ⚠️ слабо | явный local-only |
| Формат «N предложений / маркеров» | ⚠️ | дисциплина формата |
| Tool / agent черновики | частично | JSON tool-ish replies |
| Длинный deep reasoning | ❌ не цель Tiny | → Mid |

### 3.2 Suite experts (Track B) — узкие задачи

| Expert | Решает | Не решает |
|---|---|---|
| **extract** | поля, JSON, CSV hints | свободный chat |
| **summarize** | bullets, краткие протоколы | юр. заключение «с нуля» |
| **router** | выбрать эксперта | генерировать ответ сам |
| **embed** (позже) | RAG similarity | генерация текста |

### 3.3 Связь с use-cases Outpost (Commercial)

| Use-case продукта | Какая модель Lab |
|---|---|
| Analytics / ПДн offline | Tiny → Mid; extract для таблиц |
| Scribe / minutes-style | summarize specialist |
| IDE / code assist lite | Tiny (+ later code LoRA) |
| Scout / Plan (LAM) | пока BYOM 7B; Tiny как fast stage |
| Workstation Lite / weak PC | Tiny Q4 |
| Гос «допустимые веса» | любой pack с полным CARD |

---

## 4. Задачи, которые **не** обещаем Tiny

- Замена GPT-4 / облачных frontier на всех задачах
- Обучение на ПДн заказчика без договора
- Гарантия «отечественная разработка с нуля» без отдельного Mid/Large трека
- Vision/OCR как свой вес v0 (в продукте — BYOM vision)
- Unconstrained agent shell

---

## 5. Качество: определение «решили задачу»

Задача считается закрытой для версии модели, если:

1. Есть промпты в `eval/` (или suite-eval).
2. Есть rubric scores до/после.
3. GGUF грузится в Outpost (`model_loaded: true`).
4. CARD заполнен (LICENSE, SHA, base).
5. Human или явная рубрика: **pass** относительно цели релиза.

Не считается: «в чате один раз ответило красиво».

---

## 6. Ценностное предложение для заказчика (язык целей)

| Для бизнеса | Технический смысл |
|---|---|
| AI внутри периметра | GGUF + Outpost, нет cloud API |
| Понятно, что за модель | CARD + SHA + LICENSE |
| Хватает на филиал | Tiny 3B Q4 ~2 GB |
| Можно усилить центр | путь к Mid/Large (`SCALE-PLAN.md`) |
| Узкие процессы точнее | micro-MoE suite |
