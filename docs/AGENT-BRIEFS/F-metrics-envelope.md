# Brief F — Generalize the sandbox metrics envelope + golden tests

**Track:** Снять привязку ядра к спайкам, чтобы домен без SNN был возможен
**Primary repo:** `/Users/valentin/Projects/neurolab`
**Read first:** `AGENTS.md` · `docs/CLOSED-SANDBOX-CODE.md` · `docs/CLOSED-SANDBOX-MVP.md` §7 · `sandbox/src/closed_sandbox/{engine,report}.py`
**Wave:** 2026-08-08 (E–I) · orchestrator merges STATUS/ADR/INDEX

---

## Зачем этот бриф

`engine.run_project` жёстко требует от **любого** домена `spike_count`, `synops`
и `f1`/`accuracy`:

```python
required = ("spike_count", "synops", "budget_ok")
```

Экономика в `report.enrich_economy` тоже считается только через спайки, а колонки
в `write_markdown` захардкожены под них. Любой домен без спайков (оценка стоимости,
бюджет ресурсов, техпроцесс) в ядро не влезает. Это блокирует и D5+, и
переиспользование ядра.

---

## Do exactly

### 1. Обязательный минимум конверта

Оставить обязательными **только**:

| Ключ | Тип | Смысл |
|---|---|---|
| `metric_primary` | `str` | имя ключа первичной метрики |
| значение по `metric_primary` | число | сама метрика |
| `budget_ok` | `bool` | уложились во все бюджеты |

`spike_count` / `synops` / `f1` / `accuracy` — **опциональны**. Но: если домен
объявляет себя SNN-семейством (существующие D0/D1/D3/D4), требование к спайкам
сохраняется, иначе мы потеряем текущую строгость. Способ выбери сам и обоснуй в
результате — например, объявление `metrics_family` в плагине с дефолтом.

Важно: у части существующих доменов `metric_primary` может отсутствовать
(в `snn_lif` он берётся из манифеста). Разберись по факту, не по памяти, и не
ломай ни один из D0–D4 + `synapse_import`.

### 2. Экономика через манифест

`enrich_economy` сейчас умеет только `quality_per_kspike` / `quality_per_ksynop`.
Добавить обобщение:

```toml
[economy]
cost_key = "chip_power_mw"     # любой числовой ключ метрик
```

→ `quality_per_unit_cost = metric_primary / cost_key` (+ понятное имя в отчёте).
Существующие spike/synop прокси **сохранить** — они в отчётах и в
`docs/NORTH-STAR-BUILD.md` §4, ключи метрик не переименовываются никогда.

### 3. Отчёт без хардкода

`write_markdown` и таблицу `## Per scenario` сделать зависимыми от того, что
домен реально вернул, а не от фиксированного списка спайковых колонок. Домен
без спайков не должен получать колонки с `n/a`.

### 4. Golden-file тесты

Добавить в `sandbox/tests/` тесты на **точный** вид `report.md` и вывода `diff`
для одного примера (`examples/anomaly_v0`). Это защита от дрейфа формата в том
самом артефакте, который показывают заказчику. Golden-файл держи рядом с тестом.

### 5. Ничего не сломать

`cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"` должно
остаться зелёным. Сейчас там **51 passed** — меньше стать не может, только больше.
Плюс прогнать все примеры:

```bash
for p in sandbox/examples/*/project.toml; do PYTHONPATH=sandbox/src python -m closed_sandbox.cli run "$p" >/dev/null || echo "FAIL $p"; done
```

---

## Твои файлы (не выходи за них)

```text
sandbox/src/closed_sandbox/engine.py      sandbox/src/closed_sandbox/report.py
sandbox/src/closed_sandbox/manifest.py    sandbox/src/closed_sandbox/domains/**
sandbox/tests/**                          sandbox/examples/*/project.toml
```

Читать можно всё. **Писать — только в этот список.**

---

## Forbidden

- Любые `git` команды. Мержит оркестратор
- Править `STATUS.md`, `docs/DECISIONS.md`, `docs/INDEX.md`, `docs/CLOSED-SANDBOX-*.md`
- Трогать `eval/`, `scripts/`, `.gitignore` — это бриф E
- Трогать `sandbox/src/closed_sandbox/ui_server.py` и `sandbox/ui/` (отдельный трек; если обобщение требует правки UI — опиши в результате, не делай)
- Переименовывать существующие ключи метрик
- Заводить новый домен — это отдельный ADR + human
- Тянуть новые зависимости: ядро живёт на stdlib + numpy

---

## Definition of Done

- [ ] Домен без `spike_count`/`synops` проходит `run_project` (добавь минимальный тестовый плагин-фикстуру в тестах, не в `domains/`)
- [ ] Все D0–D4 + `synapse_import` работают без изменений в поведении
- [ ] `[economy] cost_key` работает, spike/synop прокси сохранены
- [ ] Golden-тесты на `report.md` + `diff`
- [ ] Unit-набор ≥ 51 passed
- [ ] `docs/AGENT-BRIEFS/results/F.md` написан

---

## Result file → `docs/AGENT-BRIEFS/results/F.md`

Обязательно включи:

1. Как именно решён вопрос строгости для SNN-семейства и почему так
2. **Черновик ADR** (кандидат NL-ADR-025) готовым текстом в формате `docs/DECISIONS.md` — оркестратор вставит
3. **Предложенную строку в STATUS Session log**
4. Число passed до и после
5. Список изменённых файлов
