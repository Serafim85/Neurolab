# Outpost Model Construct — управляемый конструктор микросетей

> **Статус:** foundation design (NL-ADR-006) — контракт и примеры сейчас; полный runtime в Outpost по мере Gate B+  
> Связано: `ARCHITECTURE.md` · `SCALE-PLAN.md` · `MICRO-MOE.md` · Commercial `MULTI-MODEL-AGENTS.md`

---

## 1. Зачем

Мы **не знаем**, куда уйдёт модельный слой: один Tiny, suite экспертов, Mid на ЦОД, vertical packs.  
Значит в основу кладём не «одну жёсткую нейросеть», а **управляемый конструкт**:

| Свойство | Смысл |
|---|---|
| **Гибкость** | менять состав экспертов без переписывания продукта |
| **Настраиваемость** | TOML/манифест: кого звать, лимиты, system, quant |
| **Масштабируемость** | тот же контракт от 1×3B до N экспертов + Mid/Large |
| **Автоподстройка** | профиль железа выбирает *какой* набор активировать |

Конструкт — это **контракт поставки и исполнения**, не новая ML-архитектура внутри одного файла весов.

---

## 2. One-liner

**Construct = каталог слотов (микросетей) + маршрутизация + политики железа + паспорт.**  
Добавил/убрал слот, сменил профиль RAM — поведение меняется; Outpost остаётся runtime.

```text
construct.toml
  ├── catalog[]     # слоты: id, path/gguf, role, ram_mb, skills
  ├── router        # rules | model | pipeline
  ├── profiles[]    # S / M / L железо → какие слоты on
  ├── policies      # load: sequential|warm|parallel; autotune
  └── provenance    # version, cards, sha
```

---

## 3. Принципы (заложить сразу)

1. **Slot, not monolith** — единица эволюции = слот (`chat`, `extract`, …), не «весь мозг».
2. **Declarative first** — состав и политики в манифесте; код Outpost читает манифест.
3. **Capability tags** — слот объявляет `skills = ["json", "ru_chat"]`; router и автоподстройка опираются на tags, не на хардкод имён.
4. **Hardware profiles** — именованные профили (`branch_8gb`, `dept_32gb`, `dc_gpu`); выбор вручную или auto.
5. **Degrade gracefully** — нет слота / мало RAM → fallback на `default` слот, не падение всего сервиса.
6. **Measure** — каждый слот со своим eval slice; конструкт versioned.
7. **YAGNI on automation** — v0: манифест + ручной profile; v1: auto profile по RAM; v2: лёгкий online tune (timeouts/slots), не «магический NAS».

---

## 4. Анатомия конструкта

### 4.1 Слот (микросеть)

| Поле | Назначение |
|---|---|
| `id` | стабильный id (`outpost-tiny`, `extract`) |
| `path` | GGUF (или URI pack) |
| `role` | `chat` \| `extract` \| `summarize` \| `router` \| `embed` \| `custom` |
| `skills[]` | capability tags |
| `ram_mb_q4` | ориентир для автоподстройки |
| `priority` | при нехватке RAM — кто выживает |
| `enabled` | можно выключить без удаления |
| `card` | путь к CARD.md |

Добавление микросети = новый `[[catalog]]` + веса + CARD.  
Удаление = `enabled = false` или drop из профиля (файл может остаться на диске).

### 4.2 Router

| Режим | Когда |
|---|---|
| `rules` | v0 — keywords / intent labels (дёшево, надёжно) |
| `pipeline` | фиксированные стадии agent (как ADR-031) |
| `model` | отдельный маленький router-GGUF |
| `hybrid` | rules first → model if low confidence |

### 4.3 Hardware profiles + autotune

```text
detect: ram_mb, cpu_threads, gpu_vram_mb (если есть)
    → choose profile
        → activate subset of slots
            → load_policy sequential|warm
```

| Profile (пример) | RAM | Активные слоты |
|---|---|---|
| `lite` | 8–16 GB | `chat` only (Tiny) |
| `standard` | 16–32 GB | `chat` + `extract` (swap) |
| `full` | 32–64 GB | + `summarize`, warm pair |
| `dc` | 64 GB+ / GPU | Mid как `chat`, suite secondary |

**Автоподстройка v1 (целевая, простая):**

1. Прочитать доступную RAM (governor / OS).  
2. Выбрать наибольший профиль, у которого `sum(priority slots peak) ≤ budget × safety_factor`.  
3. Записать в audit: `construct.profile_selected`, список enabled.  
4. Не менять профиль mid-request (только на reload / admin).

**Не делаем в v1:** online переобучение, автоподбор rank LoRA, скрытая смена модели без audit.

---

## 5. Эволюция без ломки контракта

| Этап | Состав конструкта | Что меняется |
|---|---|---|
| **C0** | 1 слот `chat` = base 3B | сейчас |
| **C1** | `chat` = Tiny LoRA | веса |
| **C2** | + `extract` + rules router | манифест |
| **C3** | + profiles lite/standard | autotune |
| **C4** | `chat` → Mid на dc profile | тот же schema |
| **C5** | vertical packs (другие skills) | новые слоты |

Семантика API Outpost (`/v1/chat`) **стабильна**; меняется только construct + веса.

```text
«Куда пойдёт нейросеть?» 
  → не новый протокол каждый раз
  → новый слот / профиль / вес под тем же Construct Schema
```

---

## 6. Разделение Lab vs Outpost

| | Neurolab | Outpost (Commercial) |
|---|---|---|
| Schema + examples | ✅ `construct/*.toml` | читает / валидирует |
| Варит GGUF слотов | ✅ | — |
| CARD / SHA | ✅ | проверяет при load |
| Router runtime | design | ✅ исполняет |
| RAM autotune | spec | ✅ governor + profile pick |
| Audit событий | — | ✅ |

Пока Gate B не готов: construct = **документированный контракт + пример**; Lab живёт с `chat`-only, Outpost — single GGUF.

---

## 7. Настройки оператора (человеком)

Оператор контура должен уметь без рекомпиляции:

- включить/выключить слот;
- сменить path на свой GGUF (BYOM slot);
- зафиксировать `profile = "lite"` (запрет auto);
- поднять `max_loaded` / `load_policy` в пределах governor;
- указать default slot при ошибке router.

Это продаётся как **управляемость**, не как «чёрный ящик одна сеть».

---

## 8. Риски и пределы гибкости

| Риск | Правило |
|---|---|
| Бесконечная конфигурация | schema versioned; неизвестные ключи — warn, не silent ignore forever |
| Автоподстройка «прыгает» | смена профиля только на старте / SIGHUP / admin API later |
| Слишком много слотов | soft cap в docs (≤6 в v1); priority eviction |
| Качество размыто | каждый слот — свой eval; construct score = weighted |

---

## 9. Минимальная реализация (порядок работ)

| Шаг | Где | DoD |
|---|---|---|
| **S0** ✅ | Lab docs + `construct/example.toml` | этот документ |
| **S1** | Lab | validate script (python/bash) для schema |
| **S2** | Lab | pack: construct.toml + ggufs layout |
| **S3** | Commercial | load construct catalog (Gate B align) |
| **S4** | Commercial | profile auto from `memory_limit_mb` |
| **S5** | Commercial | audit + ops UI «active construct» |

Не блокировать Tiny LoRA ожиданием S3–S5.

---

## 10. Связь с девизами

| Девиз | Как construct помогает |
|---|---|
| Надёжность | fallback slot; явный profile; audit |
| Качество | слоты с отдельным eval; не один «комбайн» |
| Min→max | lite profile на слабом железе; dc — когда есть ресурсы |
| Не знаем будущее | эволюция = аддитивные слоты, не rewrite |
