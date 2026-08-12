# Closed Sandbox MVP — студия мозгоподобных сетей в закрытом контуре

> **Status:** v0.1 код есть — D0–D4 + UI CS-P01…P05 в `sandbox/` (прогоны — §9)  
> **ADR:** NL-ADR-010 … 015  
> **Code:** `sandbox/`  
> **Canon (наука):** [`CLOSED-SANDBOX-CANON.md`](CLOSED-SANDBOX-CANON.md)  
> **Code canon:** [`CLOSED-SANDBOX-CODE.md`](CLOSED-SANDBOX-CODE.md)  
> **UI:** [`CLOSED-SANDBOX-UI.md`](CLOSED-SANDBOX-UI.md) · [`UI-PIPELINE`](CLOSED-SANDBOX-UI-PIPELINE.md) · [`UI-REQS`](CLOSED-SANDBOX-UI-REQS.md)  
> **Industry:** [`CLOSED-SANDBOX-INDUSTRY.md`](CLOSED-SANDBOX-INDUSTRY.md)  
> **Agents map:** [`CLOSED-SANDBOX-AGENTS.md`](CLOSED-SANDBOX-AGENTS.md)  
> **Grants:** [`CLOSED-SANDBOX-GRANTS.md`](CLOSED-SANDBOX-GRANTS.md)  
> **Verify:** [`CLOSED-SANDBOX-VERIFY.md`](CLOSED-SANDBOX-VERIFY.md)  
> Связано: `CONTOUR-EGRESS.md` · Outpost-Tiny (hammer2) · Commercial Outpost · Design Studio

---

## 1. One-liner

**Closed-contour sandbox-платформа** на стыке **нейроморфного кремния** и **био-вычислений**:  
цифровой проект → тест в песочнице (качество + энергия/ресурсы) → отчёт → `ask` (local / opt-in cloud).

**v0 код:** один домен — brain-inspired **SNN (LIF)** + anomaly.  
**Vision:** те же ядро и UX для нейрочипов *и* биотех-тем (модели вычислений на клетках/бактериях, bio-signals) — без собственной wet-lab.

Не fab. Не выращивание органоидов/бактерий у себя. Не «Adobe для всего сразу» в год 1.

---

## 2. Два слоя: платформа и домены

Общее ядро (не меняется между индустриями):

```text
project manifest → engine.run(scenarios) → metrics + report → diff → ask
```

Домены — плагины (`domain` в манифесте):

| ID | Домен | Что тестируем | Когда |
|---|---|---|---|
| **D0** | `snn_lif` | малая SNN, edge anomaly | **v0 — сейчас** |
| **D1** | `neuro_chip` | rough map/estimate · `generic_neuromorphic_v0` + **`fpga_snn_lite_v0`** | **open** (NL-ADR-020/021) |
| **D2** | `biocompute` | digital GRN toy (`boolean_grn_v0`) | **v0.1 done** (NL-ADR-022) |
| **D3** | `biosignal` | synthetic ECG/EEG → spikes → LIF | **open** (NL-ADR-023) |
| **D4** | `hybrid` | bio front → silicon SNN (composition) | **open** (NL-ADR-024) |

**Важно:** D2/D3 = симуляция и анализ данных, **не** культура клеток/бактерий in-house. Wet-lab — у партнёра; мы — контур + модели + метрики.

Стык индустрий (нейроморф ↔ биотех) = **один sandbox, разные domain packs** + общий contour `ask`.

---

## 3. Связь с Neurolab / уже сделанной сетью

| Слой | Что | Сейчас |
|---|---|---|
| **AI assistant (`ask`)** | Советы, разбор отчёта, правки манифеста | **Целевой:** hammer2 / Outpost. **Lab:** opt-in public LLM (§7). Pharma-grade R&D chat → Mid later |
| **Объект проектирования** | Зависит от `domain` (v0 = SNN) | **есть** — `sandbox/src/closed_sandbox/domains/` D0–D4 |
| **Sandbox core** | scenarios, metrics schema, report, diff | **есть** — `engine.py` / `report.py` / CLI |

Итого: Neurolab даёт ассистента. `sandbox/` — ядро платформы + первый domain pack D0.

---

## 4. Product scope

### In (v0 / MVP) — только D0

1. Манифест с полем `domain = "snn_lif"` (задел под другие домены).
2. Сеть: **SNN LIF**, бюджет нейронов/синапсов.
3. Кейс: **edge anomaly** (синтетический 1D / вибрация).
4. Metrics: F1/accuracy + spike_count / synops + latency_proxy + budget_ok.
5. Report + diff версий.
6. `ask`: `local` default | `public` opt-in.
7. CLI-first; UI later (канон: `CLOSED-SANDBOX-UI.md`).
8. Engine API так, чтобы позже добавить domain plugin **без** переписывания report/ask.

**Code status (2026-07-28):** D0 runnable under `sandbox/` — see README.

### Out (explicit non-goals v0)

- ASIC / PDK / GDSII / tape-out
- Своя wet-lab, органоиды, культивация бактерий
- Полные модели биофизики / HH / organoid intelligence as product
- Физика станков / PLC digital twin
- Все домены D1–D4 сразу
- Облачный SaaS с утечкой по умолчанию

### Later / next domains

- **D1** ✅ v0.1 estimate (`generic_neuromorphic_v0` + `fpga_snn_lite_v0`)  
- **D2** ✅ v0.1 complete (`boolean_grn_v0`)  
- **D3** ✅ synthetic ECG/EEG encode (`biosignal`)  
- **D4** ✅ hybrid composition (`front` → `snn_lif` backend) — richer fronts later  
- Более сильный contour model (Mid) для bio/pharma ask — отдельный трек

---

## 5. Архитектура кода

```text
┌─────────────────────────────────────────────────────────────┐
│  CLI / thin API                                             │
│  sandbox init | run | report | ask                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐  ┌─────────────────┐  ┌──────────────────┐
│ Project       │  │ Domain engine   │  │ Contour AI       │
│ manifest +    │  │ plugin by       │  │ local | public   │
│ domain        │  │ domain id       │  │ ask              │
└───────────────┘  └────────┬────────┘  └──────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           D0 snn_lif   D1 neuro_chip  D2 biocompute …
                        (estimate)     (later)
```

### Пакеты (целевая раскладка в `sandbox/`)

```text
sandbox/
  README.md
  pyproject.toml
  src/closed_sandbox/
    __init__.py
    manifest.py
    engine.py                 # dispatch → domain plugin
    report.py
    contour_ask.py
    domains/
      snn_lif/                # D0
      neuro_chip/             # D1 estimate (NL-ADR-020)
      # biocompute/           # later
      # biosignal/            # later
  examples/
    anomaly_v0/
      project.toml
      data/
    chip_estimate_v0/
      project.toml
      fixtures/
  tests/
```

Язык v0: **Python 3.11+**. Новый домен = пакет + запись в каноне/ADR, не форк репо.

---

## 6. Манифест проекта (черновик схемы)

```toml
[project]
id = "anomaly-v0"
name = "Vibration anomaly SNN"
version = "0.1.0"
domain = "snn_lif"          # D0; later: biocompute | biosignal | neuro_chip | hybrid

[network]
kind = "snn_lif"            # must match domain in v0
n_inputs = 16
n_hidden = 64
n_outputs = 2
neuron = "lif"
dt_ms = 1.0

[budget]
max_neurons = 128
max_synapses = 4096
# proxy caps for sandbox fail/warn
max_spikes_per_sample = 5000

[task]
kind = "binary_anomaly"
dataset = "examples/anomaly_v0/data"
metric_primary = "f1"

[sandbox]
scenarios = ["nominal", "anomaly", "noise"]
seed = 42

[contour]
ask_enabled = true
# provider: "local" (default for pilots) | "public" (lab/dev opt-in only)
provider = "local"
base_url = "http://127.0.0.1:8090/v1"
model = "outpost-tiny-hammer"

# --- lab/dev only: uncomment + set env; never commit keys ---
# provider = "public"
# base_url = "https://api.openai.com/v1"   # or other OpenAI-compatible
# model = "gpt-4o-mini"
# api_key_env = "CLOSED_SANDBOX_LLM_API_KEY"
```

Новый `domain` / `kind` = ADR + строка в `CLOSED-SANDBOX-CANON.md`.

---

## 7. Метрики sandbox (обязательные)

| Метрика | Зачем |
|---|---|
| `f1` / accuracy | Качество на задаче |
| `spike_count` | Proxy энергии (ниже = лучше при той же F1) |
| `synops` | Proxy compute |
| `latency_proxy_ms` | Грубая оценка (sim time или event rate) |
| `budget_ok` | Уложились ли в max_neurons/synapses/spikes |

Таблица выше — контракт **семейства `snn`** (D0/D1/D3/D4), а не всех доменов. Ядро требует только
`metric_primary` + значение + `budget_ok`, поэтому неспайковый домен законен и не обязан возвращать
`spike_count` / `synops` (NL-ADR-025 · канон: [`CLOSED-SANDBOX-CODE.md`](CLOSED-SANDBOX-CODE.md) §3).
Domain-specific поля (`resource_proxy`, `circuit_size`, …) добавляются сверху, а `metric_primary` +
report/diff остаются общими.

DoD прогона: JSON metrics + короткий markdown report. Без метрик — прогон не засчитывается (как eval в Lab).

---

## 8. Contour AI (ассистент) — local default, public opt-in

Политика = `CONTOUR-EGRESS.md` (зоны Local / Client cloud / Public LLM).

| Режим | Когда | Как |
|---|---|---|
| **`provider = local`** | пилоты, demo, «закрытый контур» | Outpost / hammer2 на `127.0.0.1` (или client-private endpoint) |
| **`provider = public`** | **ранняя разработка**, пока local слаб / нет GPU | OpenAI-compatible API; ключ только из env; **явный opt-in** |

Правила:

1. **Default в коде и в example-манифестах = `local`.** Public не включается «молча».
2. Public: предупреждение в CLI (*данные манифеста/отчёта уйдут к провайдеру*); audit-лог provider + host (не тело промпта по умолчанию).
3. Ключи: env (`CLOSED_SANDBOX_LLM_API_KEY` и т.п.), **никогда в git / project.toml**.
4. `run` / metrics / report **не зависят** от ИИ — работают offline всегда.
5. Если `local` и Outpost не запущен — `ask` падает с инструкцией (или подсказывает переключить на public для lab).
6. Продуктовый story и гранты: целевой режим = closed contour; public = scaffolding, не GTM-обещание «всё в облаке».

---

## 9. Definition of Done — sandbox v0.1

- [x] `project.toml` валидируется (`domain = snn_lif`)
- [x] engine диспатчит в `domains/snn_lif` (задел под другие domain packs)
- [x] `closed-sandbox run examples/anomaly_v0` отрабатывает на synthetic data
- [x] Report с F1 + spike_count + budget_ok
- [x] `closed-sandbox diff` двух version dirs (CLI + tests)
- [x] `closed-sandbox ask` → local Outpost smoke (`pytest -m integration`)
- [ ] `ask` с `provider=public` — код + unit на missing key; live public optional
- [x] `tests/` unit + integration (см. [`CLOSED-SANDBOX-VERIFY.md`](CLOSED-SANDBOX-VERIFY.md))
- [x] Нет секретов / больших датасетов в git
- [x] Запись в `STATUS.md` Session log

**Verified 2026-08-08:** unit **85 passed** (`-m "not integration"`, 3 deselected;
было 51 до wave 2). Шлюз: `bash scripts/gate.sh` (6 steps, GATE: PASS); CI —
`.github/workflows/ci.yml`. Integration в этот прогон **не запускался** — нужен
Metal/GPU host + Commercial release `sovereignd`; последний зелёный прогон — 2026-07-28.

**Verified 2026-07-28:** unit **11 passed**; integration **3 passed** (host Mac).

Полный лист прогонов: [`CLOSED-SANDBOX-VERIFY.md`](CLOSED-SANDBOX-VERIFY.md).

---

## 10. План кодинга (первые 2 недели)

| Дни | Результат |
|---|---|
| 1–2 | package skeleton + `domains/` layout, manifest (`domain`), example `project.toml` |
| 3–5 | minimal LIF forward + synthetic anomaly dataset |
| 6–8 | engine metrics + markdown/JSON report |
| 9–10 | version diff + CLI |
| 11–12 | contour_ask: local Outpost + opt-in public provider |
| 13–14 | tests, README how-to, STATUS update |

Один рычаг за итерацию: сначала engine+metrics, потом ИИ-хук.

---

## 11. Гранты / юрисдикция

Не блокер кодинга. Полная карта: **[`CLOSED-SANDBOX-GRANTS.md`](CLOSED-SANDBOX-GRANTS.md)**.

Кратко:

- S1 после демо: national / Innosuisse / Eurostars (и Pathfinder с uni).  
- S2: Chips JU (консорциум), Transition*.  
- S3: **EIC Accelerator Open** (Challenges 2026 — не AI).  
- Кандидат на жизнь/паспорт: Люксембург — отдельно от кода.  
- Правило: измеримый продукт → деньги; наоборот не работает.

---

## 12. Граница репозиториев

| Что | Где |
|---|---|
| Прототип студии, SNN engine, examples, docs | **neurolab `sandbox/`** |
| Веса ассистента, eval, LoRA | neurolab как сейчас |
| Продуктовый daemon/UI/pilot pack | Commercial Outpost (когда созреет) |
| Fab / EDA / industrial physics | не здесь |

Смена границы → ADR.
