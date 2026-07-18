# План масштабирования

От минимальных ресурсов к мощным весам в контуре — без прыжка в foundation на дне 1.

---

## 1. Принцип масштабирования

```text
качество на узком @ 3B
    → suite экспертов @ 1.5–3B   (новые слоты construct)
        → Mid 7–14B (тот же слот chat, другой path / profile dc)
            → Large / MoE (ЦОД)
```

Масштабирование = **обогащение конструкта** (слоты, профили, веса), не смена протокола.  
См. `CONSTRUCT.md` стадии C0–C5.

На каждом шаге: **eval gate** + **CARD** + **бюджет compute**.  
Не масштабируем размер, пока не выжали качество с текущего.

**Min resource → max result:** сначала данные и LoRA, потом параметры; железо режет активные слоты через profiles.
---

## 2. Уровни (L)

Совместимо с Commercial ADR-018 / `MODEL-SOVEREIGNTY-PATH.md`.

| L | Артефакт | RAM (Q4 orient.) | Условие входа |
|---|---|---|---|
| **L0** | Upstream GGUF BYOM | любое | сейчас ✅ |
| **L1** | Curated pack + паспорт | = upstream | SHA + LICENSE bundle |
| **L2** | Vertical LoRA | ≈ base | paying pilot / vertical data |
| **L3** | **Outpost-Tiny** 1.5–3B | ~2–4 GB | baseline + LoRA pass ← **мы здесь** |
| **L4** | Suite micro-MoE (2–4 GGUF) | peak = largest if swap | extract pass |
| **L5** | **Outpost-Mid** 7–14B | ~8–12 GB | Tiny ceiling + demand |
| **L6** | Outpost-Large 30–70B / arch-MoE | 40 GB+ | ЦОД + бюджет |
| **L7** | Pretrain с нуля | extreme | юр/гео требуют; партнёр |

---

## 3. Дорожная карта (практическая)

### Phase N0 — Foundation Lab ✅ / in progress

- [x] Repo + agent docs
- [x] Locked base 3B + baseline 14/16
- [ ] LoRA data (refuse + format)
- [ ] Tiny-v0/v1 adapt → re-eval

### Phase N1 — Tiny shippable

- Merge LoRA → GGUF `outpost-tiny-v1`
- Handoff checklist (`INTEGRATION.md`)
- Optional: Commercial curated note

### Phase N2 — Micro-MoE lite

- Expert `extract` only
- Router = rules in agents.toml
- Sequential load on Outpost Gate B

### Phase N3 — Mid

- Choose 7B or 14B base (LICENSE!)
- SFT/LoRA under same eval culture
- Positioning: «мощная контурная» для госа

### Phase N4 — Scale-out

- Large on GPU server
- Consider arch-MoE only if dense Mid plateau + hardware ready
- Industry packs (gov / analytics / scribe)

---

## 4. Ресурсы (ориентир)

| Этап | Compute | Данные | Люди |
|---|---|---|---|
| Baseline / eval | Mac CPU/Metal, уже есть | 8 prompts | 1 |
| LoRA Tiny | 1×24 GB GPU или Colab; CPU LoRA — last resort | 1k–20k pairs | 1 |
| Extract expert | same | узкий JSON set | 1 |
| Mid 14B | multi-GPU / rented | larger instruct | 1 + optional partner |
| Large | cluster / SI partner | serious corpus | partner |

Правило: **не арендовать Mid-кластер**, пока Tiny-v1 не закрыл gap baseline.

---

## 5. Масштабирование качества (не только размера)

| Рычаг | Когда | Стоимость |
|---|---|---|
| Лучшие промпты / system | всегда сначала | низкая |
| Eval expansion | каждый релиз | низкая |
| LoRA data mix | H1 | средняя |
| Rank / epochs | после data | средняя |
| Больше params | H3+ | высокая |
| Arch-MoE | H4 | очень высокая |

---

## 6. Масштабирование suite

```text
v0: chat-tiny only
v1: + extract
v2: + summarize
v3: + LM router (если rules ошибаются >X%)
v4: vertical packs (разные LoRA на одном backbone)
```

Одновременно в RAM: по возможности **1** модель (swap). Warm pair — только на 32 GB+ серверах (Commercial governor).

---

## 7. Критерии «пора увеличивать размер»

Переходить 3B → 7B+, если **все** верны:

1. Tiny-v1 стабильно на eval и ручных сценариях.
2. Есть 3+ задачи, где Tiny систематически ≤1/2 при хороших данных.
3. Есть железо заказчика / наше под Mid.
4. Human подтвердил приоритет vs suite experts.

Иначе: ещё данные / specialist, не «накачать параметры».

---

## 8. Риски масштабирования

| Риск | Митигация |
|---|---|
| Размытие фокуса | один L-шаг за квартал внимания |
| Overfit eval | держать holdout prompts |
| LICENSE сюрприз | CARD review до train |
| Cost spiral | LoRA-first budget cap |
| GTM overpromise | packs только из STATUS Done |
