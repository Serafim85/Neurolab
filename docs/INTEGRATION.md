# Встраивание в Outpost

Как артефакты Нейролаб попадают в продукт и контур заказчика.

---

## 1. Принцип

```text
Neurolab готовит файл + паспорт
        ↓
Outpost загружает как обычный GGUF (BYOM / curated pack)
        ↓
Клиенты (Web / CLI / TUI / IDE) не знают, «своя» модель или нет —
они бьют в /v1/chat/completions
```

Дифференциация — в **supply chain и CARD**, не в отдельном протоколе.

---

## 2. Точки встраивания (куда)

| Точка | Когда | Как |
|---|---|---|
| **`[models].path`** | сразу после первого Tiny GGUF | путь к файлу в `sovereign.toml` |
| **Curated pack / bundle** | после стабильного Tiny-v1 | файл + LICENSE + SHA в offline bundle |
| **Preset `sovereign model pull`** | optional | добавить preset id в Commercial (ADR) |
| **Agent stage `model_id`** | Gate B multi-model | Tiny / extract на разных стадиях |
| **Workstation Lite** | ADR-019 | Tiny как единственная модель на слабом ПК |
| **Default demo model** | GTM decision | только human; не менять без STATUS |

Не встраиваем:

- Python training в daemon
- Отдельный «neurolab microservice» в пилоте
- Замену llama.cpp

---

## 3. Сейчас (H0 / H1)

### 3.1 Eval / Lab smoke

```bash
# Lab daemon (не prod)
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  ~/Projects/neurolab/config/sovereign.baseline.toml
# → http://127.0.0.1:8090
./scripts/run_baseline.sh
```

### 3.2 Ручной BYOM в Commercial

```toml
# AI-Platform-Vision/sovereign.toml (пример)
[models]
path = "/Users/valentin/Projects/neurolab/artifacts/base/Qwen2.5-3B-Instruct-Q4_K_M.gguf"
```

После LoRA — путь на `artifacts/outpost-tiny-v1-*.gguf`.

### 3.3 Что уже совместимо

| Outpost capability | Tiny pack |
|---|---|
| `/v1/chat/completions` | ✅ |
| ChatML template | ✅ (`chat_template = "chatml"`) |
| CLI / TUI / Web | ✅ через тот же API |
| `parallel_slots` | ✅ (N копий одной модели) |
| Vision mtmd | ❌ отдельный BYOM + mmproj |
| Multi-model agents | 🔜 Gate B — тогда suite |

---

## 4. Handoff checklist (Lab → Commercial)

Перед тем как считать pack «готовым к продукту»:

- [ ] GGUF в `artifacts/` (не в git)
- [ ] `SHA256` записан в CARD и `artifacts/.../SHA256.txt`
- [ ] LICENSE base + заметка об адаптации
- [ ] Eval sheet: scores vs baseline
- [ ] Smoke: `health.model_loaded` + 3 ручных промпта в Outpost
- [ ] Запись в neurolab `STATUS.md` Done
- [ ] Human: текст для SI / не overpromise
- [ ] Optional ADR в Commercial при смене default preset

---

## 5. Construct + Micro-MoE в продукте

```text
neurolab/construct/example.toml  (+ pack construct.toml)
neurolab artifacts/*.gguf
        ↓
Outpost loads construct (Gate B+ target)
  profile auto|lite|… → active slots
  router → slot
  fallback → defaults.slot
```

Пока runtime construct не в Commercial: эквивалент — `agents.toml` catalog + pipelines (`MULTI-MODEL-AGENTS.md`).  
Манифест Lab — **superset** и целевой pack format (`docs/CONSTRUCT.md`).

До Gate B: один active GGUF; слоты `extract`/`summarize` готовим в Lab с `enabled = false`.
---

## 6. Контур заказчика (air-gap)

1. Lab (connected) варит GGUF + CARD PDF/md.
2. Носитель USB / внутреннее зеркало.
3. На сервере Outpost: положить файл, прописать path, checksum.
4. `sovereign model pull` на prod **не** использовать.

Политика: Commercial `docs/MODEL-BYOM.md`.

---

## 7. Версионирование артефактов

| Поле | Пример |
|---|---|
| Model id | `outpost-tiny-v1` |
| Filename | `outpost-tiny-v1.Q4_K_M.gguf` |
| CARD | `models/outpost-tiny/CARD.md` |
| Eval tag | `eval/results/tiny-v1-vs-baseline.md` |

Semver модели **не** обязан совпадать с semver Outpost runtime.
