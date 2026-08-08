# Архитектура Нейролаб → Outpost

> Канон для агентов. Связано: `GOALS.md` · `INTEGRATION.md` · `SCALE-PLAN.md` · Commercial `MODEL-SOVEREIGNTY-PATH.md`

---

## 1. One-liner

**Нейролаб проектирует и варит веса; Outpost исполняет их offline.**  
Архитектура «сети» на старте — **плотный decoder-only LLM** (база Qwen2.5); эволюция — через **Model Construct** (слоты микросетей + профили железа), не через разовую монолитную клятву.

Полный контракт гибкости: **`docs/CONSTRUCT.md`** + `construct/example.toml`.  
Интеллектуальная база линейки: **`docs/INTELLECTUAL-CANON.md`**.---

## 2. Два слоя архитектуры

### 2.1 Системная (Lab + Product)

```text
┌─────────────────────────────────────────────────────────────┐
│  Нейролаб (этот repo)                                       │
│  cards · datasets manifests · train/export · eval · packs   │
└───────────────────────────┬─────────────────────────────────┘
                            │ GGUF + CARD + SHA + LICENSE
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Outpost / sovereignd (Commercial)                          │
│  llama.cpp · /v1/chat · agents · audit · governor · UI/CLI  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    контур заказчика (air-gap)
```

Нейролаб **не** содержит inference-сервера как продукт. Daemon на `:8090` — только для **eval smoke**.

### 2.2 Модельная (что внутри «своей нейросети»)

| Уровень | Сейчас (v0) | Позже |
|---|---|---|
| **Семейство** | Qwen2 (decoder-only, dense) | то же семейство или совместимое |
| **Размер** | ~3B Instruct + Q4_K_M | Tiny distill 1.5B · Mid 7–14B · Large |
| **Адаптация** | none → LoRA / light SFT | vertical LoRA, multi-adapter |
| **Токенизатор** | базовый Qwen (не свой) | свой только при жёсткой необходимости |
| **Формат поставки** | GGUF | GGUF (+ mmproj отдельно для vision BYOM) |
| **«MoE»** | нет в весах | product suite (отдельные GGUF) → опционально arch-MoE на Large |

**Решение:** не проектируем новую transformer-архитектуру с нуля в v0–v1. Меняем **поведение и supply chain**, опираясь на проверенный dense backbone.

---

## 3. Целевая модель Outpost-Tiny (v0)

```text
┌──────────────────────────────────────────┐
│  Outpost-Tiny                            │
│  backbone: Qwen2.5-3B-Instruct (dense)   │
│  adapt: LoRA (rank 8–16) или light SFT   │
│  export: merge → GGUF Q4_K_M             │
│  chat template: ChatML (как в Outpost)   │
└──────────────────────────────────────────┘
```

| Параметр | Значение v0 |
|---|---|
| Params | ~3B |
| Quant | Q4_K_M (~1.8 GB) |
| Context (lab) | 4k |
| Context (prod target) | 4k–8k |
| Sampling eval | temperature 0.2, max_tokens 256 |
| Locked base SHA | см. `artifacts/base/SHA256.txt` |

Подробный паспорт: `models/outpost-tiny/CARD.md`.

---

## 4. Model Construct + Micro-MoE

Не слои MoE внутри одного чекпоинта, а **управляемый конструкт** — каталог слотов, которые можно добавлять/убирать/настраивать:

```text
construct.toml
    profiles (lite → dc) ── autotune by RAM/GPU
            │
            ▼
       active slots[] ◄── enable/disable / BYOM path
            │
            ▼
         router (rules → model)
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
  chat  extract  summarize   … future slots
```

Каждый слот — **dense** GGUF (+ CARD). Исполнение в Outpost: ModelPool / agents (ADR-031), load_policy sequential|warm.

| Документ | Что |
|---|---|
| `docs/CONSTRUCT.md` | гибкость, профили, автоподстройка, эволюция |
| `construct/example.toml` | schema v0.1 |
| `docs/MICRO-MOE.md` | мотивация suite экспертов |
---

## 5. Потоки данных (Lab)

```text
datasets/ (manifests only in git)
    │
    ▼
train / LoRA  ──► checkpoints/ (local, gitignored)
    │
    ▼
merge + convert ──► artifacts/*.gguf
    │
    ▼
eval/prompts + RUBRIC ──► eval/results/
    │
    ▼
CARD.md update (SHA, provenance)
    │
    ▼
handoff → Commercial pack / BYOM path
```

**Audit:** при smoke через Outpost — `artifacts/baseline-audit.jsonl` (метаданные; prompt content off by default).

---

## 6. Current focus → STATUS

**Текущий фокус здесь не описан.** Единственный источник — [`../STATUS.md`](../STATUS.md)
§Summary + §Next; этот документ отвечает за топологию, а не за то, что делается сегодня.

Принцип, который от фокуса не зависит: следующий уровень лестницы открывается
только после измеренного результата на текущем — `docs/SCALE-PLAN.md`.  
Куда именно в продукт: `docs/INTEGRATION.md`.

---

## 7. Нефункциональные требования архитектуры

| NFR | Как обеспечиваем |
|---|---|
| **Reliability** | воспроизводимый pull/SHA; один скрипт baseline; CARD обязателен |
| **Quality** | rubric 0–2; pass bar vs baseline; gaps → train data |
| **Min resources** | LoRA > full FT; 3B > 14B until proven need; 1 GPU/Colab ok |
| **Security / contour** | нет ПДн в git; LICENSE + provenance; offline GGUF |
| **Operability** | dense + llama.cpp path only for v0–v1 |

---

## 8. Границы ответственности компонентов

| Компонент | Владелец | Ответственность |
|---|---|---|
| Backbone weights (upstream) | Qwen / HF mirror | pretrain |
| LoRA / SFT / export | **Neurolab** | поведение, pack |
| Inference engine | **Outpost** | load, sample, API |
| Router in production | **Outpost** agents | кого звать |
| Eval design | **Neurolab** | что считать качеством |
| GTM claims | Human + Commercial docs | не врать про «свою 70B» |

---

## 9. Диаграмма решений (что не трогаем)

```text
[ ] Новый tokenizer
[ ] Свой attention / matmul
[ ] Arch-MoE v0
[ ] Train в commercial crate
[x] Dense Qwen2.5-3B + LoRA
[x] GGUF + Outpost smoke
[x] Product micro-MoE suite (позже)
```
