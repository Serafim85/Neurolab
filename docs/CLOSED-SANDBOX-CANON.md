# Closed Sandbox Canon — мозгоподобные сети (SNN / neuromorphic)

> **Статус:** living canon (NL-ADR-011) · обновлять при крупных сдвигах, не каждую неделю  
> **Продукт:** `CLOSED-SANDBOX-MVP.md` · код: `sandbox/` · агенты: `CLOSED-SANDBOX-AGENTS.md`  
> **Рядом:** код [`CLOSED-SANDBOX-CODE.md`](CLOSED-SANDBOX-CODE.md) · индустрия [`CLOSED-SANDBOX-INDUSTRY.md`](CLOSED-SANDBOX-INDUSTRY.md)  
> **Фильтр:** усиливает **edge / energy proxy / closed contour / измеримый sandbox**  
> Не путать с `INTELLECTUAL-CANON.md` (линейка Outpost dense LLM).

---

## 1. Зачем отдельный **научный** канон

Рамка MVP говорит *что строим*. Научный канон говорит *на чём думаем в модели*:

1. Какие уроки биологии/нейронауки **берём** в инженерию.  
2. Что **откладываем** (биофизическая точность ≠ продукт v0).  
3. Какие стартапы/платформы — ориентиры, не объект копирования.  
4. Что читать команде перед сменой `network.kind` или метрик.

Канон **не заменяет** sandbox metrics. Нет F1/spike_count → идея из paper не принята.

---

## 2. Столпы (ДНК Closed Sandbox)

| Столп | Откуда | Как у нас в v0 |
|---|---|---|
| **Spikes / events** | биологические action potentials; Maass «3rd gen» | SNN, не непрерывный ANN-активатор |
| **Разреженность во времени** | мозг активен локально и редко | proxy energy = `spike_count` / synops |
| **Простой нейрон first** | LIF — стандартный инженерный компромисс | `snn_lif` only в v0 |
| **Edge, не datacenter** | EdgeSNN surveys 2025 | anomaly / sensor-like задача |
| **ПО до fab** | фрагментация железа; нет «CUDA для SNN» | studio + sim; map to chip later |
| **Closed contour** | sovereignty / privacy edge | целевой `ask` = Outpost; public LLM = **opt-in lab only** (`CONTOUR-EGRESS`) |
| **Measure** | NeuroBench / lab doctrine | report обязателен |

**Девиз:** вдохновляемся мозгом для **энергии и событийности**; не обещаем «воспроизвели кору».

---

## 3. Adopt / Defer (биология → инженерия)

| Идея из науки | Adopt? | Как в продукте |
|---|---|---|
| Импульсы вместо плотного matmul | **Adopt** | SNN forward, event accounting |
| Энергия ~ активность | **Adopt** | метрика spike_count / synops |
| Адаптация online | **Defer** (v0) | fixed/trained offline; online later |
| STDP / биологическая пластичность | **Defer** | surrogate grad / ANN→SNN проще для MVP |
| Дендриты, нейромедиаторы, глия | **Defer** | out of scope |
| Predictive coding / free energy | **Watch** | интересно для v1+; не блокер |
| Liquid NN (C. elegans–inspired) | **Defer** | другой `kind`, отдельный ADR |
| Organoid / wetware **как своя лаба** | **Out** | не выращиваем ткань/бактерии in-house |
| Цифровые модели biocompute (GRN / bacterial circuit abstractions) | **Adopt D2 toy** | `boolean_grn_v0` (NL-ADR-022); wet-lab still out |
| Biosignal / MEA event pipelines | **Watch → later D3** | стык биотех↔SNN без wet-lab |
| Hybrid bio-data → silicon SNN | **Adopt D4 composition** | `hybrid` NL-ADR-024; synthetic front only for now |
| Memristor-accurate synapse | **Defer** | железо later; в sim не моделируем drift |
| Полная биофизика (HH) | **Defer** | LIF достаточно для studio v0 |

Смена строки Adopt→другое = правка этого файла + запись в Session log (или ADR, если меняется `domain` / `network.kind`).

---

## 3b. Bio adjacency (стык с биотехом)

Платформа рассчитана на **два промышленных берега**, один core:

| Берег | Примеры объектов в sandbox | Наша роль |
|---|---|---|
| Нейроморф / edge AI | SNN, neuro_chip estimates | D0 → **D1 open** (NL-ADR-020 · proxy only) |
| Биотех / био-вычисления | GRN toy models, bacterial compute abstractions, biosignals | D2 done · **D3 open** |
| Стык | MEA/sensor events → SNN; сравнение bio vs silicon proxies | **D4 open** (synthetic); partner MEA later |

**Не делаем:** культура клеток, GMP, organoid farm, синтез ДНК in-house.  
**Делаем:** модели, метрики, контур, позже ingest данных партнёра.

---

## 4. Книги и учебники

### Tier A — must для команды sandbox

| Источник | Зачем |
|---|---|
| **Gerstner, Kistler, Naud, Paninski — *Neuronal Dynamics*** (online) · [neuronaldynamics.epfl.ch](https://neuronaldynamics.epfl.ch/) | LIF, синапсы, популяции — общий язык |
| **Maass, W. (1997)** — Networks of spiking neurons: the third generation… | зачем spikes как вычислительная модель |

### Tier B — по мере углубления

| Источник | Зачем |
|---|---|
| **Dayan & Abbott — *Theoretical Neuroscience*** | если лезем глубже в learning rules |
| **Indiveri / Liu surveys** (neuromorphic circuits) | мост к железу, когда появится map-to-chip |
| **Goodfellow / Prince** (из INTELLECTUAL-CANON) | общий ML-фундамент; не дублировать здесь |

### Tier C — продукт / systems

| | |
|---|---|
| Chip Huyen — *Designing ML Systems* | данные, eval, итерации — тот же дух, что ENGINEERING.md |

---

## 5. Статьи и обзоры (якорные)

Не библиотека — **якоря**. Перед цитированием в гранте перепроверьте год/DOI.

| Работа | Тема | Наш вывод |
|---|---|---|
| **Edge Intelligence with Spiking Neural Networks** (survey, 2025) · [arXiv:2507.14069](https://arxiv.org/abs/2507.14069) | EdgeSNN: нейроны, обучение, железо, бенчмарки | подтверждает вертикаль edge + нужду в честных метриках |
| **SNN training / hardware / apps survey** (AI Sensors etc., 2025) | ANN→SNN, surrogate grad, STDP, Loihi/SpiNNaker/… | v0: surrogate или conversion; STDP later |
| **Comparative DNN vs SNN for edge neuromorphic circuits** · [PMC12528140](https://pmc.ncbi.nlm.nih.gov/articles/PMC12528140/) | energy/area trade-offs, зрелость tooling | честно: tooling слабее DNN — наш moat = studio UX + contour |
| **SNN Architecture Search survey** (2025) · [arXiv:2510.14235](https://arxiv.org/abs/2510.14235) | NAS под energy/latency | не делаем NAS в v0; budget в манифесте — ручной рычаг |
| **Zenke & Ganguli — SuperSpike** (и линия surrogate gradient) | обучение многослойных SNN | путь обучения, когда выйдем за ручные веса |
| **Davies et al. — Loihi** (IEEE Micro) | neuromorphic manycore | ориентир железа, не зависимость v0 |
| **NeuroBench** (initiative / papers) | бенчмарки neuromorphic | later: сравниваться; v0 = свой report schema |

Добавление якоря: 1 абзац «зачем нам» + Adopt/Defer. Без этого — не в канон.

---

## 6. Похожие стартапы / платформы (ориентиры)

Цель таблицы — **ландшафт**, не «копируем фичи».

| Игрок | Что делают | Урок для нас |
|---|---|---|
| **Innatera** (Pulsar) | neuromorphic MCU, edge sensing | ниша: сенсоры + ultra-low power; мы — **ПО-студия**, не чип v0 |
| **BrainChip** (Akida) | digital SNN inference | есть железо → later export/target |
| **SynSense** | event-based / SNN edge | vision/event path; наш первый кейс — 1D anomaly |
| **SpiNNcloud** | large-scale neuromorphic compute | science/supercomputer; не наш buyer |
| **Polyn** | analog NASP, µW sensing | подтверждает sensor-edge деньги; сложный analog — defer |
| **GrAI Matter / snap-era** | edge AI graph | рынок edge тесный; дифференциация = contour + design loop |
| **FinalSpark / Cortical Labs** | organoid / biological computers | **out** нашего scope; другой риск/этика |
| **NIR** (Neuromorphic Intermediate Representation) | portable SNN IR | watch: интеграция later, не invent CUDA |
| **Intel Lava**, **Nengo** | frameworks | можно опереться/интегрировать; v0 может быть тонким своим engine |

**Наша щель:** closed-contour **design → sandbox → report → ask**, не продажа своего ASIC в год 1.

---

## 7. Что это значит для кода (жёстко)

| Решение | Канон говорит |
|---|---|
| `network.kind = snn_lif` | да, v0 |
| Метрики без spike proxy | нет |
| Тянуть HH / мультикомпартмент | нет, пока нет ADR |
| Облачный LLM как **единственный** режим ask | нет (default = local) |
| Opt-in public LLM для ранней разработки | да (явный `provider=public` + env key) |
| Заявлять «биологически точная модель мозга» | нет |
| Читать Gerstner + EdgeSNN survey перед сменой kind | да |

---

## 8. Как обновлять

1. Новый paper/startup → секция 3 или 5–6 + дата в Session log.  
2. Смена Adopt/Defer на столпе → коротко в STATUS; смена `kind` → ADR.  
3. Не раздувать канон дайджестами новостей; только то, что влияет на продукт.

---

## 9. Связь с другими доками

| Док | Роль |
|---|---|
| `CLOSED-SANDBOX-MVP.md` | *что* строим и DoD |
| **этот файл** | *почему* так в науке (adopt/defer) |
| `CLOSED-SANDBOX-CODE.md` | *как* писать код |
| `CLOSED-SANDBOX-UI.md` | *как выглядит* инструмент |
| `CLOSED-SANDBOX-INDUSTRY.md` | *для кого* / стандарты / конкуренты |
| `CLOSED-SANDBOX-GRANTS.md` | *куда* за грантами по стадиям |
| `CLOSED-SANDBOX-AGENTS.md` | ритуал чтения для агентов |
| `INTELLECTUAL-CANON.md` | dense LLM / Outpost-Tiny (hammer2 как ассистент) |
| `CONTOUR-EGRESS.md` | политика контура для `ask` |
| `ENGINEERING.md` | цикл measure → change → eval |
