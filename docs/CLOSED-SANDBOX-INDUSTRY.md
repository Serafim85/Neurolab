# Closed Sandbox — индустриальный канон

> **Статус:** living (2026-07-28) · NL-ADR-013  
> **Рядом:** научный [`CLOSED-SANDBOX-CANON.md`](CLOSED-SANDBOX-CANON.md) · продукт [`CLOSED-SANDBOX-MVP.md`](CLOSED-SANDBOX-MVP.md)  
> **Фильтр:** покупатели, стандарты, конкуренты, стык **нейроморф ↔ биотех** — без wet-lab in-house и без fab-мечты в год 1.

---

## 1. Зачем индустриальный канон

Научный канон отвечает *что верно в модели*.  
Индустриальный — *кому продаём, с чем стыкуемся, кого не копируем вслепую*.

Агенты читают этот файл перед:

- формулировкой value prop / гранта;  
- выбором vertical (anomaly vs biosignal vs biocompute);  
- «давайте как компания X».

---

## 2. Позиционирование (одна фраза)

**Closed-contour design & test studio** for compact brain-inspired / event-driven compute models — starting with SNN — with a path to **neuro-chip estimates** and **digital biocompute / biosignal** domains.  
Not a foundry. Not an organoid farm. Not a public-LLM SaaS by default.

---

## 3. Кто платит (buyer map)

| Сегмент | Боль | Наш клин | Стадия |
|---|---|---|---|
| **Edge / industrial sensing** | энергия, latency, air-gap | D0 anomaly SNN + report | v0–v1 |
| **Neuromorphic integrators** | трудно пробовать SNN до железа | D0→D1 map/estimate | v1 |
| **Medtech / biosignal R&D** | нельзя слать сигналы в облако | D3 + contour ask | v1+ |
| **Biotech / synthetic bio (compute)** | нужны *модели* схем до мокрого опыта | D2 digital biocompute | v1+ |
| **Pharma / neuro R&D IT** | контур + ассистент | Mid LLM track + sandbox tools | отдельно от D0 |
| **Defense / critical infra** | sovereignty | contour default local | later, compliance-heavy |

Первый платящий гипотетический buyer: **edge sensing / industrial anomaly**, не «все биотех-лаборатории Европы».

---

## 4. Стандарты и стыки (ориентиры)

Не изобретать «свой CUDA». Стыковаться или watch:

| Слой | Стандарт / экосистема | Наш статус |
|---|---|---|
| SNN portability | **NIR** (Neuromorphic Intermediate Representation) | Watch → later export |
| Neuromorphic SW | Intel **Lava**, **Nengo**, vendor SDKs (Akida…) | Watch; v0 свой thin engine |
| Benchmarks | **NeuroBench** | Later сравнение; v0 свой report schema |
| Edge ML (ANN world) | ONNX, TFLite | Не цель D0; bridge later if ANN→SNN |
| Bioelectronics data | MEA formats / open ephys-класс (по партнёру) | D3 ingest later |
| Contour / security | EU AI Act risk framing, air-gap practice | Policy: `CONTOUR-EGRESS.md` |
| Semicon design (далеко) | PDK / EU Design Platform | Out of v0; partner only |

Правило: новый внешний формат = plugin/adapter, не переписывание core.

---

## 5. Конкуренты и ориентиры (не клоны)

| Игрок | Индустрия | Урок | Не делать |
|---|---|---|---|
| Innatera, BrainChip, SynSense | neuromorphic silicon | edge + energy real | свой ASIC в год 1 |
| Polyn | analog edge | µW sensing | analog physics in v0 sim |
| SpiNNcloud | large neuromorphic | science scale | supercomputer product |
| FinalSpark / Cortical Labs | wetware / organoid | PR + research | своя культура ткани |
| Cadence / Synopsys | EDA | UX сложности | «Photoshop для GDSII» |
| NVIDIA Isaac / digital twin vendors | industrial sim | sandbox UX | копировать Omniverse |
| Benchling / bio informatics suites | biotech software | data contour | подменять ELN |

**Наша щель:** design→test→report→ask в **одном контуре**, dual-domain road (silicon + digital bio), измеримые energy proxies.

---

## 6. Стык двух индустрий (как говорить с рынком)

```text
Нейроморфный берег          Биотех-берег
SNN / neuro_chip     ←→     biocompute / biosignal
         \                 /
          \               /
           Closed Sandbox core
           (metrics, report, contour)
```

Честные формулировки:

- «Тестируем **цифровые** модели био-вычислений и event pipelines» — да.  
- «Делаем вычисления на живых бактериях у себя» — нет.  
- «Партнёр даёт MEA/sensor data → мы считаем в контуре» — да (D3/D4).  
- «Заменяем Cadence + GMP lab» — нет.

---

## 7. Качество «промышленной базы» для агентов

Перед фичей спросить:

1. Какой **buyer** из §3?  
2. Какой **domain** (D0–D4)?  
3. Есть ли **метрика** приёмки?  
4. Есть ли **стандарт/конкурент** в §4–5, с которым не конфликтуем?  
5. Не нарушаем ли wet-lab / fab out-of-scope?

Если «нет buyer» и «нет метрики» — не кодить, backlog в STATUS.

---

## 8. Связь с грантами

Индустриальный narrative для EU/CH: **edge energy + sovereignty + ECS tools** (± health biosignal later).  
Детали программ: `CLOSED-SANDBOX-GRANTS.md`.  
Не обещать tape-out или organoid factory в заявке v0.

---

## 9. Обновление

- Новый конкурент / стандарт → 1 абзац сюда + дата в STATUS.  
- Смена primary buyer → правка §3 + Session log.  
- Не превращать файл в дайджест новостей.
