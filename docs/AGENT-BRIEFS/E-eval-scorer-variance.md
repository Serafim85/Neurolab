# Brief E — Automated eval scorer + variance (highest-value lever)

**Track:** Сделать главный измерительный прибор лаборатории воспроизводимым
**Primary repo:** `/Users/valentin/Projects/neurolab`
**Read first:** `AGENTS.md` · `eval/agent-rubric.md` · `eval/README.md` · `scripts/run_agent_eval.py`
**Wave:** 2026-08-08 (E–I) · orchestrator merges STATUS/ADR/INDEX

---

## Зачем этот бриф

Сейчас `scripts/run_agent_eval.py` только собирает ответы модели — **скорера не
существует**, все оценки во всех `eval/results/*.md` поставлены руками. Плюс один
прогон при `temperature 0.2` без повторов. При шкале 0/1/2 на 10 промптов один
промпт весит 10% результата, а решения принимались по ±1 («pb 16/20 (−1) → не
продвигать»). Такие дельты неотличимы от шума сэмплирования.

В песочнице этот урок уже выучен: `closed-sandbox stress` гоняет 20 seed и
докладывает mean±stdev. Задача — принести ту же дисциплину на модель.

---

## Do exactly

### 1. `scripts/score_agent_eval.py`

Детерминированный скорер по `eval/agent-rubric.md`. Рубрика уже сформулировала
машинно-проверяемые критерии — используй их буквально:

| id | Механическая проверка |
|---|---|
| `tool_json` | тело — только валидный JSON-объект, ключи `tool`/`args`, без markdown-обёртки |
| `tool_json_args` | то же + `args.path`, `args.max_bytes` |
| `schema_extract` | валидный JSON, **точные** ключи `host`/`ram_gb`/`role` |
| `router_hint` | одна метка из `extract`/`chat`/`summarize`, без прозы |
| `budget_sentences` | **ровно 2** предложения |
| `plan_steps` | 3–5 нумерованных строк, без эссе |
| `plan_tool_mix` | первая строка — метка `plan`, далее ≤4 нумерованных шага |

Остальные (`code_lite`, `refuse_public`, `self_check`) — семантические.
Для них: эвристика с явной пометкой `needs_human: true` в выводе. **Не
притворяйся, что оцениваешь их машинно.**

Требования к скореру:

- Вход: каталог с `all.jsonl` (формат из `run_agent_eval.py`) **или** отдельные `<id>.txt`
- Выход: `score.json` (per-id: score 0/1/2, reason, needs_human) + короткий markdown
- Шкала и агрегат ровно как в рубрике: max = 2×N, докладывать `score / 20`
- Чистая stdlib, без сети, детерминированно

### 2. Повторы и разброс

Расширь `scripts/run_agent_eval.py`:

- `--repeats N` (default 1), `--temperature` default **0.0** (было 0.2)
- при N>1 писать `all.jsonl` со полем `repeat`
- скорер при N>1 докладывает **mean ± stdev** и `score_min` / `score_max`

Формат вывода держи как в `closed-sandbox stress` — та же дисциплина, тот же вид.

### 3. Валидация на реальных данных (это и есть DoD)

Локально есть записанные прогоны в `eval/results/raw/*/`. Прогони скорер на них
и **сверь с оценками, выставленными руками** в соответствующих
`eval/results/agent-v0-*.md`.

Доложи в результате таблицу: id → рука → скорер → совпало?
Расхождения не замазывай — они самое ценное в этом брифе. Если скорер
воспроизводит 16/17/20 по машинным id — прибор годен.

### 4. Сырьё в git

В `.gitignore` открой доказательную базу (сейчас `eval/results/raw/` закрыт целиком):

```gitignore
eval/results/raw/**
!eval/results/raw/*/
!eval/results/raw/*/all.jsonl
!eval/results/raw/*/meta.json
!eval/results/raw/*/score.json
```

Проверь через `git check-ignore` что per-prompt `.txt`/`.json` дампы остаются вне
git, а `all.jsonl` / `meta.json` / `score.json` — внутри. **Не делай `git add`.**

### 5. Тесты

`tests/test_score_agent_eval.py` (создай каталог `tests/` в корне): фикстуры на
каждый машинный id — pass, fail, и граничный случай (JSON в markdown-обёртке →
не 2). Запуск: `python -m pytest tests -q` из корня.

### 6. `eval/README.md`

Короткая секция: как собрать, как оценить, как читать mean±stdev. Одна команда
на шаг.

---

## Твои файлы (не выходи за них)

```text
scripts/score_agent_eval.py      scripts/run_agent_eval.py
tests/                           eval/README.md
.gitignore                       eval/results/raw/*/score.json
```

Читать можно всё. **Писать — только в этот список.**

---

## Forbidden

- Любые `git` команды: add / commit / push / checkout. Мержит оркестратор
- Править `STATUS.md`, `docs/DECISIONS.md`, `docs/INDEX.md`, `eval/agent-rubric.md`
- Трогать `sandbox/` — это бриф F
- Запускать GPU-тренировку или менять GGUF
- Подгонять скорер под «красивое» число: если рука и скорер расходятся, это находка, а не баг скорера по умолчанию
- Ставить `needs_human: false` семантическим id ради полной автоматизации

---

## Definition of Done

- [ ] `score_agent_eval.py` работает на записанных `eval/results/raw/*/`
- [ ] Таблица «рука vs скорер» с объяснением каждого расхождения
- [ ] `--repeats` + temperature 0 + mean±stdev
- [ ] `python -m pytest tests -q` зелёный
- [ ] `git check-ignore` подтверждает: `all.jsonl` в git, per-prompt дампы нет
- [ ] `docs/AGENT-BRIEFS/results/E.md` написан

---

## Result file → `docs/AGENT-BRIEFS/results/E.md`

Обязательно включи:

1. Таблицу «рука vs скорер» и вывод: годен ли прибор
2. Какие id остались семантическими и почему
3. **Предложенную строку в STATUS Session log** (2–6 строк) — оркестратор вмержит
4. Команду проверки одной строкой
5. Список изменённых файлов
