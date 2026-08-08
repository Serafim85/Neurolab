# Result I — CI + шлюз одной командой

> **Brief:** [`I-ci-and-gate.md`](../I-ci-and-gate.md) · **Date:** 2026-08-08 · **Status:** done
> Git не трогал: ни `add`, ни `commit`, ни `push`. Мержит оркестратор.

---

## 1. Вывод `scripts/gate.sh` (как сейчас)

```text
neurolab gate · 2026-08-08T16:41:42
root: /Users/valentin/Projects/neurolab
commit: b9ad090
python: Python 3.12.7

OK    sandbox unit tests           19s
OK    sandbox examples              3s
OK    demo pack (D0-D4)             6s
OK    doc links                     0s
OK    eval scorer smoke             0s
OK    root tests                    1s

steps: 6 ok · 0 fail · 0 skip
GATE: PASS
```

`exit=0`. Полный прогон ~30 s, GPU и Commercial-бинари не нужны.

Проверено отдельно (обе ветки, а не «по логике»):

| Сценарий | Как проверял | Результат |
|---|---|---|
| `SKIP`, а не `FAIL` | scratch-root без `tests/` и без `score_agent_eval.py` | `4 ok · 0 fail · 2 skip` → `GATE: PASS` |
| `FAIL` виден целиком | scratch-root с намеренно битой ссылкой | шаг `FAIL`, вывод шага напечатан, `GATE: FAIL`, `exit=1` |
| Шлюз не встаёт на первом провале | тот же scratch | после `FAIL` прошли оставшиеся шаги, потом вердикт |

### Что делает каждый шаг

| # | Шаг | Команда | Поведение при отсутствии |
|---|---|---|---|
| 1 | sandbox unit tests | `cd sandbox && PYTHONPATH=src pytest -q -m "not integration"` | — |
| 2 | sandbox examples | `cli run` по всем 7 `examples/*/project.toml` (`--seed 42`) | — |
| 3 | demo pack | `bash sandbox/scripts/demo_pack.sh` (**вызов, не правка**) | — |
| 4 | doc links | `python3 scripts/check_doc_links.py` | — |
| 5 | eval scorer | `--selftest` если есть, иначе smoke интерфейса | `SKIP` |
| 6 | root tests | `pytest tests -q` | `SKIP` |

**Отклонение от брифа (осознанное):** в брифе у шлюза 5 шагов, я добавил шестой —
корневой `pytest tests`. Причина: DoD брифа требует, чтобы отсутствие `tests/`
давало `SKIP`, а без этого шага условие нечем проверить, и «единый шлюз» не
покрывал бы набор трека E. Нумерация 1–5 сохранена.

**Шаг 5 честнее, чем звучит.** Скорер трека E появился прямо во время работы и
`--selftest` не имеет, поэтому шаг называется `eval scorer smoke` и доказывает
только, что CLI грузится. Настоящее покрытие скорера — 56 тестов в `tests/`
(шаг 6). Если E добавит `--selftest`, шлюз сам переключится на него и напишет
`eval scorer selftest`.

### Гонка с параллельными треками

Юнит-набор песочницы на старте сессии дал **51 passed / 3 deselected** (как в
брифе), в конце — **85 passed / 3 deselected**. Прогон шёл одновременно с
треками F/H, которые добавляли тесты; чужой код я не трогал и «не чинил».
3 deselected — это integration, они отфильтрованы маркером, а не сломаны.

---

## 2. Битые ссылки в документах

**Markdown-ссылок битых нет: 0.**

```text
scanned 55 markdown files · 142 relative links checked · 29 external/anchor-only skipped
note: anchors (FILE.md#section) are not validated, only the file part
result: OK
```

Что проверяется: относительные `[text](target)`, `![alt](target)` и
reference-определения `[label]: target` в `docs/**/*.md`, `AGENTS.md`,
`STATUS.md`, `README.md`. Содержимое fenced-блоков и inline-кода исключено
(иначе примеры команд давали бы ложные срабатывания). Якоря не валидируются —
проверяется только файловая часть `FILE.md#section`; валидация якорей означала
бы красный CI на каждое переименование заголовка.

Что тулза **точно ловит** (проверено на подсадной странице): битый относительный
путь, битый путь с якорем, битое reference-определение; и не ловит того, чего
не надо — внешние URL и ссылки внутри code fence.

### Побочная находка: 0 битых ссылок ≠ 0 битых упоминаний

В этом репозитории документы ссылаются друг на друга в основном **бэктиками**, а
не markdown-ссылками (карта документов в `AGENTS.md`, таблицы в STATUS). Я
прогнал разовый аудит таких упоминаний: 390 путей в бэктиках, из них 61 не
существует по пути от корня репозитория.

Гейтить это **нельзя**, и в тулзу я это не добавил — почти всё «отсутствующее»
корректно, просто путь не от корня neurolab:

| Класс | Пример | Почему это не поломка |
|---|---|---|
| Пути Commercial-репозитория | `config/sovereign.pilot-contour-gate.toml`, `scripts/synapse-gate-smoke.sh`, `docs/MODEL-BYOM.md` | существуют в `~/Projects/AI-Platform-Vision`, в тексте помечены словом «Commercial» — проверил все три |
| Пути репозитория `synapse` / `design` | `design/studio/manifest.json`, `synapse/docs/COMPOSE.md` | другой репозиторий |
| Пути относительно `sandbox/` | `tests/test_snn_lif.py`, `out/metrics.json`, `parity/CS-P03.yaml` | существуют, но глубже |
| Плейсхолдеры | `artifacts/runs/YYYYMMDD-HHMMSS/NOTES.md` | шаблон, не файл |
| Ещё не созданное | `docs/CLAIMS.md`, `scripts/gen_model_card.py` | треки G/H этой же волны |

**Что с этим делать (решение человека, не моё):** ложных срабатываний слишком
много, чтобы это гейтить. Если такие упоминания хочется проверять, сначала
нужна конвенция — например, префикс `Commercial:` / `synapse:` / `sandbox/`
перед путём, — и только потом скрипт. Сейчас это дороже пользы.

---

## 3. Вопрос человеку: LICENSE

`LICENSE` я **не создавал** — это решение владельца, а не агента. Отсутствие
файла на GitHub означает «all rights reserved»: смотреть можно, использовать
нельзя, и это не обязательно то, что ты хочешь.

Три варианта:

| # | Вариант | Последствия |
|---|---|---|
| **1** | **Ничего не делать** (репозиторий приватный, лицензии нет) | Максимальная защита IP по умолчанию. Но: при любом внешнем доступе (грант, инвестор-due-diligence, подрядчик) статус кода читается как «нельзя ничего», и вопрос всё равно всплывёт. Стоимость сейчас: 0; стоимость потом: срочное решение под дедлайн |
| **2** | **Явный proprietary-файл** `LICENSE` = «Copyright (c) 2026 …, All rights reserved. Internal use only» | То же самое юридически, но написано словами. Снимает вопрос на due diligence, ничего не открывает, обратим в любую сторону. Дешевле всего и рекомендуемый дефолт, если открывать пока не планируешь |
| **3** | **Раздельная лицензия:** код песочницы (`sandbox/`, `scripts/`) под Apache-2.0, документы и модели — proprietary | Даёт то, что просят грантовые программы (EIC / Chips JU / Innosuisse — см. `docs/CLOSED-SANDBOX-GRANTS.md`) и позволяет пилоту читать код. Взамен: Apache-2.0 необратим для уже опубликованных версий, нужен NOTICE и дисциплина «что в каком каталоге» |

**Важно вне зависимости от выбора:** лицензия репозитория **не** покрывает веса.
Адаптеры и GGUF наследуют условия базовой модели, а в
`models/outpost-tiny/CARD.md` upstream LICENSE записан как **MISSING** («Do not
assume Apache-2.0»). Пока это не закрыто (трек H), любой permissive-LICENSE на
репозиторий рискует читаться как разрешение на веса, которого нет.

Вопрос коротко: **вариант 1, 2 или 3 — и планируется ли вообще внешний доступ к
коду в ближайшие полгода?**

---

## 4. Lock-файл: как собрать и зачем (не собирал)

`requirements-train.lock` вслепую на этой машине не генерировал: это Apple
Silicon, а train-бокс — CUDA, и `torch` у них принципиально разные колёса.
Лок, снятый здесь, на CUDA-машине не поставится.

Зачем он нужен: `requirements-train.txt` состоит из `>=`-диапазонов, то есть
через полгода `pip install -r` соберёт другой стек. Обучение, воспроизводимость
которого зависит от даты установки, — это не воспроизводимость. Лок делает
«повторить тот же train» проверяемым утверждением, а не надеждой.

Как собрать — **на том железе, где реально учат**, в чистом venv:

```bash
python3.11 -m venv /tmp/lock-venv && source /tmp/lock-venv/bin/activate
pip install --upgrade pip
pip install -r requirements-train.txt
pip freeze --exclude-editable > requirements-train.lock
deactivate && rm -rf /tmp/lock-venv
```

Практические оговорки:

1. **Лок платформозависим.** Честно — два файла: `requirements-train.cuda.lock`
   (train-бокс) и `requirements-train.macos-arm64.lock` (лаборатория). Один
   общий будет ложью для одной из машин.
2. `pip freeze` не пишет источник колеса. Для CUDA-сборок в шапку файла нужен
   комментарий с `--index-url` (например `https://download.pytorch.org/whl/cu121`).
3. Хочешь строже — `pip-tools` (`pip-compile --generate-hashes`) даёт хеши; цена
   — ещё одна зависимость в контуре.
4. В CI лок **не нужен**: раннер ставит только `numpy` + `pytest` из
   `sandbox/pyproject.toml`, train там не бывает.

---

## 5. Предлагаемая строка в STATUS Session log

Оркестратору — вставить в `STATUS.md` § Session log (я файл не трогал):

```markdown
### 2026-08-08 — CI + шлюз одной командой (трек I)

- **Goal:** «measure first» как исполняемый шлюз, а не ритуал на память
- **Done:** `.github/workflows/ci.yml` (push/PR, ubuntu, Python 3.11+3.12, без GPU
  и Commercial); `scripts/gate.sh` — 6 шагов, одна строка `GATE: PASS/FAIL`;
  `scripts/check_doc_links.py` (stdlib); `docs/ENGINEERING.md` §9–10
- **Verify:** `bash scripts/gate.sh` → `GATE: PASS` (6 ok / 0 fail / 0 skip, ~30 s);
  `python3 scripts/check_doc_links.py` → 142 ссылки, 0 битых
- **Scores:** sandbox unit 51 → 85 passed (рост от треков F/H, не от I); битых
  markdown-ссылок 0/142
- **Next:** решение человека по LICENSE (3 варианта в `docs/AGENT-BRIEFS/results/I.md`);
  `requirements-train.lock` — снять на train-боксе; `--selftest` в скорере (трек E)
```

### Строка в `docs/INDEX.md`

Отдельная строка для ENGINEERING уже есть (стр. 32); предлагаю только уточнить
описание, чтобы шлюз находился поиском:

```markdown
| [`ENGINEERING.md`](ENGINEERING.md) | Цикл, code style, логи, DoD · **шлюз `scripts/gate.sh` + CI** |
```

### ADR — предлагаю не писать

Отдельный ADR не нужен: новых архитектурных развилок нет, это исполнение уже
принятых девизов. Если оркестратор всё же хочет запись — одной строкой
«CI и pack-шлюз: `scripts/gate.sh`, integration и GPU вне CI осознанно».

---

## 6. Изменённые файлы

| Файл | Что |
|---|---|
| `.github/workflows/ci.yml` | новый — push/PR, ubuntu-latest, Python 3.11 + 3.12 |
| `scripts/gate.sh` | новый — единый шлюз, 6 шагов, `GATE: PASS/FAIL` (executable) |
| `scripts/check_doc_links.py` | новый — проверка ссылок, только stdlib (executable) |
| `docs/ENGINEERING.md` | §8 чеклист + строка шлюза; новые §9 «Шлюз» и §10 «CI» |
| `docs/AGENT-BRIEFS/results/I.md` | этот файл |

За пределы списка «Твои файлы» не выходил. `sandbox/**`, `eval/`, `.gitignore`,
`STATUS.md`, `AGENTS.md`, `docs/DECISIONS.md`, `docs/INDEX.md`, `models/` — не
трогал.

### Что в CI и почему именно это

Шаги: установка `sandbox[dev]` → «нет весов в индексе» → doc links → unit-тесты
(`-m "not integration"`) → все примеры → `tests/` (если есть, иначе печатает
`SKIP`).

- **Матрица 3.11 + 3.12.** 3.11 — минимум из `sandbox/pyproject.toml`, 3.12 —
  лабораторная машина. Иначе они разъедутся молча.
- **Шаг «нет весов в индексе»** (`*.gguf`, `*.safetensors`, `*.ckpt`, `*.pt`,
  `*.pth`) — небольшая добавка сверх брифа: это первый пункт review-чеклиста
  `ENGINEERING.md` §8, и он единственный, который нельзя починить после пуша.
- **`|| true` нигде нет.** Отсутствие `tests/` — это `if [ -d tests ]`, а не
  проглоченная ошибка; упавший шаг падает и показывает вывод.
- **Integration (3 теста) в CI нет** — комментарий в шапке workflow объясняет
  почему (нужны `sovereignd` release + GGUF + Metal) и как гонять локально,
  чтобы никто не «починил» их добавлением.
- **`demo_pack.sh` в CI отдельным шагом нет** — он гоняет 6 из тех же примеров,
  что уже покрыты шагом «Sandbox examples». В локальном шлюзе он есть, потому
  что это ровно тот сценарий, который показывают инвестору.

Все шаги CI прогнаны локально построчно (`bash -eo pipefail`), YAML распарсен.
Чего проверить нельзя без пуша: сам факт запуска Actions на `Serafim85/Neurolab`
(нужно, чтобы Actions были включены в настройках репозитория) и `pip install -e
"./sandbox[dev]"` на чистом Linux-раннере (локально ставить не стал, чтобы не
менять окружение).

---

## 7. Требует решения человека

1. **LICENSE** — вариант 1 / 2 / 3 (§3). Блокирует любые внешние обещания про код.
2. **Upstream LICENSE весов** — в CARD стоит `MISSING`; пока так, permissive
   лицензия на репозиторий опасна (§3, трек H).
3. **`requirements-train.lock`** — снять на train-боксе, скорее всего два файла
   под две платформы (§4).
4. **Actions включены?** Проверить в настройках `Serafim85/Neurolab`; при первом
   пуше workflow должен появиться во вкладке Actions.
5. **Ветка `master`.** Триггер `on: push` без фильтра ветки — специально, чтобы
   работало и после переименования в `main`. Если появится branch protection,
   required check называется `gate`.
