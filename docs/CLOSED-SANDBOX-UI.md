# Closed Sandbox — канон интерфейса (UI/UX)

> **Статус:** living (2026-07-28) · NL-ADR-014 / 015  
> **Продукт:** [`CLOSED-SANDBOX-MVP.md`](CLOSED-SANDBOX-MVP.md) · агенты: [`CLOSED-SANDBOX-AGENTS.md`](CLOSED-SANDBOX-AGENTS.md)  
> **Конвейер:** [`CLOSED-SANDBOX-UI-PIPELINE.md`](CLOSED-SANDBOX-UI-PIPELINE.md) · **FR:** [`CLOSED-SANDBOX-UI-REQS.md`](CLOSED-SANDBOX-UI-REQS.md)  
> **Рядом:** код [`CLOSED-SANDBOX-CODE.md`](CLOSED-SANDBOX-CODE.md) · индустрия [`CLOSED-SANDBOX-INDUSTRY.md`](CLOSED-SANDBOX-INDUSTRY.md)  
> **Фильтр:** интерфейсы для **инженеров / учёных / edge-R&D**, не consumer SaaS-тренды.

---

## 1. Будет ли интерфейс?

**Да.** Порядок поставки:

| Этап | UI | Зачем |
|---|---|---|
| **v0.1** | CLI + markdown/JSON report | измеримый engine без UI-долга |
| **Design** | Design Studio: Lab → Prod ★ | FR + макеты **до** кода UI |
| **v0.2** | локальный web UI (thin) | Port после ★ + parity ≥90% |
| **v1+** | multi-domain workspace | вкладки/домены D0–D4, сравнение версий |

CLI не отменяется: всё, что видно в UI, должно быть достижимо из CLI (автоматизация, air-gap скрипты, грантовые демо).

**Запрет:** кодить production UI без FR id и без макета в Design Studio (категория Closed Sandbox). Конвейер = Commercial `DESIGN-TO-PROD.md`, адаптированный в `CLOSED-SANDBOX-UI-PIPELINE.md`.

Агенты **не** рисуют «красивый лендинг» вместо sandbox. UI = инструмент контура.

---

## 2. Столпы UI (ДНК)

1. **Workflow > chrome** — экран вокруг цикла `project → run → report → ask`, не вокруг маркетинга.  
2. **Progressive disclosure** — сначала Run / Metrics / Fail reasons; advanced (neuron params, raw spikes) по запросу.  
3. **Situation awareness** — за 3 секунды: прошёл ли прогон, F1, energy proxy, budget_ok, provider ask (local/public).  
4. **Consistency** — цвет/иконка alarm ≠ декорация; одни и те же метрики в CLI report и UI.  
5. **Error prevention > clever recovery** — валидация манифеста до run; ясные блокировки.  
6. **Longevity** — UI на годы; не гнаться за glassmorphism / purple gradients / emoji-first.  
7. **Contour honesty** — если `provider=public`, **видимый** баннер риска утечки; local = спокойный статус.  
8. **Density for experts** — таблицы и графики плотные; whitespace как в Notion-лендинге — не наш канон.  
9. **Keyboard & reproducibility** — hotkeys, copy manifest hash, export report one click.  
10. **One job per view** — Overview / Editor / Run+Metrics / Ask / Diff — не дашборд «всё сразу».

---

## 3. Информационная архитектура (целевая)

```text
[Projects] → [Editor: manifest + domain]
                    ↓
              [Run console]
                    ↓
         [Results: metrics | plots | logs]
           ↙                ↘
     [Diff versions]     [Ask assistant]
```

| View | Обязательный контент |
|---|---|
| Overview | список проектов, last F1 / spike_count / status |
| Editor | TOML (or form+raw), domain badge, budget caps |
| Run | seed, scenarios, progress, cancel |
| Results | metric cards + spike/time plot + download JSON/MD |
| Diff | side-by-side metrics + changed manifest keys |
| Ask | chat + attached report; provider chip (local/public) |

v0.2 может склеить Editor+Run+Results в один экран с секциями — но **логические зоны** те же.

---

## 4. Лучшие примеры (ориентиры, не клоны)

Смотреть *поведение* и иерархию, не копировать бренд.

### 4.1 Научные / инженерные инструменты

| Пример | Почему смотреть | URL / где |
|---|---|---|
| **ParaView** | научный viz: pipeline, progressive detail | https://www.paraview.org/ |
| **Napari** | плотный scientific viewer, Python-native | https://napari.org/ |
| **ImageJ / Fiji** | возраст + мощь: меню под workflow учёного | https://imagej.net/ |
| **JupyterLab** | клеточный workflow; осторожно — не превращать sandbox в notebook-only | https://jupyter.org/ |
| **Grafana** | metrics-first dashboards, alarm semantics | https://grafana.com/ |
| **Weights & Biases / MLflow UI** | run → metrics → compare (близко к нашему Diff) | https://mlflow.org/ · https://wandb.ai/ |

### 4.2 EDA / electronics / «сложные системы»

| Пример | Почему смотреть | URL / где |
|---|---|---|
| **KiCad** | open EDA: схемы/платы, expert density | https://www.kicad.org/ |
| **Analog Devices / vendor eval UIs** | datasheet→параметры→график (простая правда) | vendor tools |
| **Cadence Virtuoso** (как антипример UX) | мощь ценой когнитивной нагрузки — **не** копировать меню-ад | industry standard |
| **VS Code** | editor+panel+terminal; хорошая модель «инструмент, не сайт» | https://code.visualstudio.com/ |

### 4.3 Lab / bio / industrial HMI

| Пример | Почему смотреть | URL / где |
|---|---|---|
| **Benchling** (bio R&D SaaS) | научный workflow + данные; взять структуру, не облачный default | https://www.benchling.com/ |
| **SnapGene** | ясная научная визуализация последовательностей | https://www.snapgene.com/ |
| **High Performance HMI** (process industry) | уровни экранов, цвет только для alarm | ISA-101 / books §5 |
| **LabVIEW** (как антипример современности) | wire spaghetti — урок «не путать мощь с ясностью» | NI |

### 4.4 Близко к neuromorphic / edge

| Пример | Почему смотреть |
|---|---|
| Vendor SDKs (**BrainChip MetaTF**, **Innatera** tooling, **Lava** tutorials) | как показывают spikes/energy; взять ясность метрик |
| **NeuroBench** reporting style | честное сравнение accuracy vs energy |

Правило: если пример **cloud-first** или **consumer** — заимствовать только IA, не визуальный язык.

---

## 5. Книги и учебники (Tier)

### Tier A — must перед серьёзным UI

| Книга | Зачем нам |
|---|---|
| **Tamara Munzner — *Visualization Analysis and Design*** | научный viz: что кодировать каналами, ложь графиков, task-driven design |
| **Edward Tufte — *The Visual Display of Quantitative Information*** | плотность данных, chartjunk = враг |
| **Bill Hollifield et al. — *The High Performance HMI Handbook*** | промышленный HMI: уровни экранов, alarm color discipline |
| **ISA-101** (Human Machine Interfaces for Process Automation) | индустриальный стандарт мышления об HMI |

### Tier B — interaction & product

| Книга | Зачем |
|---|---|
| **Don Norman — *The Design of Everyday Things*** | affordance, feedback, ошибки |
| **Alan Cooper et al. — *About Face* (interaction design)** | goals personas → screens; для expert tools |
| **Stephen Few — *Information Dashboard Design*** | метрики на одном экране без карнавала |
| **Chrisopher Wickens et al. — *Engineering Psychology and Human Performance*** | нагрузка внимания, situation awareness (глубже) |

### Tier C — по необходимости

| | |
|---|---|
| **Colin Ware — *Information Visualization*** | восприятие, 3D/2D tradeoffs |
| **Victor Lombardi — *Why We Fail* / postmortems UX** | осторожно с «интуитивностью» для экспертов |
| Научные UX notes (MD+DI life-science UX) | lab software longevity, hierarchy of tasks |

Не нужны как канон: чисто marketing UI kits, «SaaS landing» гайды.

---

## 6. Визуальный язык (черновые правила)

| Тема | Правило |
|---|---|
| Цвет | нейтральная база; **цвет = статус/alarm/metric threshold**, не бренд-радуга |
| Typography | читаемые mono для манифеста/логов; UI sans с нормальным tabular nums для метрик |
| Dark/light | поддержка обеих; научные графики часто dark-ok |
| Motion | минимум; только progress/run state |
| Cards | только если несут действие (Run, Ask); Results — table+plot first |
| Empty states | «Run example anomaly-v0» одной кнопкой, не onboarding-карусель |
| i18n | UI strings EN first (как код); RU docs отдельно |

Анти-паттерны (явно запрещены как default):

- purple-on-white AI aesthetic;  
- hero marketing blocks внутри app;  
- pill soup / stat strip без drill-down;  
- скрытый public LLM без баннера.

---

## 7. Связь с доменами

| Domain | UI-акцент |
|---|---|
| D0 `snn_lif` | spike raster / count, F1, budget |
| D1 `neuro_chip` | estimate cards (power/area proxy), export status |
| D2 `biocompute` | circuit/graph view + resource proxy (не «лабораторный 3D ради красоты») |
| D3 `biosignal` | timeline events, encode preview |
| D4 `hybrid` | two-pane bio→silicon pipeline |

Один chrome — разные **result widgets** по domain plugin (как CODE: thin core, fat plugins).

---

## 8. DoD для UI-работы

- [ ] Тот же scenario проходится в CLI и даёт те же metrics  
- [ ] Contour provider виден всегда при Ask  
- [ ] Нет секретов в localStorage / телеметрии наружу (default)  
- [ ] Results: export JSON + MD  
- [ ] Ссылка на этот канон / пример из §4 в Session log, если меняли IA  
- [ ] Не ломает air-gap путь (static или local server)

---

## 9. Когда агенту читать этот файл

- Любая работа над web UI / layout / plots  
- Выбор component library  
- «Сделаем как ChatGPT / Notion / Figma» — сначала этот канон (скорее **нет**)  
- Добавление domain-specific visualization

Порядок: **MVP workflow → UI canon → CODE plugin widgets → INDUSTRY buyer**.
