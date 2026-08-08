# Инженерный подход, стиль, логи

**Девизы:** надёжность · качество · минимум ресурсов → максимум результата.

---

## 1. Инженерный цикл (обязательный)

```text
1. Hypothesis (одна)
2. Baseline / current score
3. Change (данные XOR гиперпараметры XOR base)
4. Train / export GGUF
5. Eval (RUBRIC) + Outpost smoke
6. CARD + STATUS + Session log
7. Keep or revert
```

Нет шага 2 или 5 → эксперимент не засчитывается.

---

## 2. Definition of Done (любая модельная задача)

- [ ] Измеримый результат в `eval/results/` или явный N/A с причиной
- [ ] CARD обновлён (если веса/адаптация)
- [ ] Скрипт воспроизведения (bash/python) в `scripts/` или команды в CARD
- [ ] Нет секретов / ПДн / `.gguf` в git
- [ ] `STATUS.md` Session log
- [ ] Отклонения от ARCHITECTURE → ADR

---

## 3. Code style

### 3.1 Языки

| Язык | Где | Стиль |
|---|---|---|
| **Bash** | `scripts/*.sh` | `set -euo pipefail`; абсолютные пути или `ROOT=`; help при ошибке |
| **Python** | train / parse eval | 3.10+; type hints на публичных функциях; no bare `except:` |
| **Markdown** | docs / CARD | заголовки, таблицы; даты ISO `YYYY-MM-DD` |
| **TOML** | config для Outpost | комментарии why; абсолютные path для Lab smoke |
| **JSONL** | eval prompts / datasets manifests | один объект на строку; стабильные `id` |

Rust inference **не** пишем здесь (Commercial).

### 3.2 Имена

- Файлы скриптов: глагол `pull_base.sh`, `run_baseline.sh`, `train_lora_tiny.sh`
- Модели: `outpost-<role>-v<N>`
- Eval id: `snake_case` стабильный навсегда (`ru_airgap`)
- Ветки git (если появятся): `feat/…`, `fix/…`, `docs/…`

### 3.3 Комментарии

- Только **why** (лицензия, воспроизводимость, safety).
- Код и идентификаторы — **English**; docs могут быть RU (как сейчас).

### 3.4 Ошибки и надёжность скриптов

- Проверять наличие GGUF / daemon / binary до долгого train.
- Явные exit codes; сообщение «что сделать дальше».
- Не глотать stderr train-утилит.
- Идемпотентность: повторный `pull` без `--force` не затирает молча (как Commercial CLI).

### 3.5 Минимализм

- Нет абстракций «на трёх экспертов вперёд».
- Нет второго eval framework, пока `prompts.ru.jsonl` + rubric хватает.
- Rule of Three: третий дубль → вынести helper.

---

## 4. Логи для агентов

### 4.1 Обязательные артефакты лога сессии

| Артефакт | Где |
|---|---|
| Session log | `STATUS.md` § Session log |
| ADR (если решение) | `docs/DECISIONS.md` |
| Eval numbers | `eval/results/*.md` |
| Raw model outputs | `eval/results/raw/` (gitignored ok) |
| Train command + seed | CARD или `artifacts/runs/<stamp>/NOTES.md` |

### 4.2 Формат Session log

```markdown
### YYYY-MM-DD — <title>

- **Goal:** …
- **Done:** …
- **Verify:** команды / пути
- **Scores:** before → after (если eval)
- **Next:** …
```

### 4.3 Формат run notes (train)

`artifacts/runs/YYYYMMDD-HHMMSS/NOTES.md`:

```markdown
# Run …
base: …
lora_rank: …
data: …
epochs: …
export: path/to.gguf
sha256: …
eval: link to results
```

### 4.4 Outpost audit

При smoke: `artifacts/baseline-audit.jsonl` — **не** включать `log_prompt_content` без нужды (как Commercial security baseline).

### 4.5 Что агент пишет всегда

1. Изменение CARD / STATUS при смене весов или scores.
2. Если эксперимент провален — тоже в лог (чтобы не повторять).

---

## 5. Качество и надёжность (девизы в практике)

| Девиз | Практика |
|---|---|
| **Качество** | rubric 0–2; holdout; gaps → data, не vibes |
| **Надёжность** | SHA; pinned base; скрипт > ручной click; повторный baseline |
| **Min resources** | LoRA; 3B; один GPU; не parallel suite train |
| **Max result** | закрывать GTM/контурные gaps (refuse, format, JSON) первыми |

---

## 6. Данные

- В git: только manifests (`datasets/*.md`, списки URL, LICENSE notes).
- Корпуса — локально / USB; путь в NOTES.
- Запрет: реальные ПДн пилота, секреты, внутренние отчёты заказчика.
- Предпочтение: open instruct + **синтетика** под gaps.

---

## 7. Безопасность Lab

- Нет обязательного bind кроме localhost для smoke.
- Не публиковать GGUF с неясной LICENSE.
- Private remote для neurolab (когда появится).
- Не логировать полные промпты в shared каналы.

---

## 8. Review checklist перед merge/commit

- [ ] `bash scripts/gate.sh` → `GATE: PASS` (закрывает первые три пункта ниже)
- [ ] `.gguf` не в индексе
- [ ] Скрипты executable + `set -euo pipefail`
- [ ] Docs ссылки не битые (относительные пути)
- [ ] STATUS обновлён
- [ ] Одна логическая тема на commit

---

## 9. Шлюз: `scripts/gate.sh`

Девиз «measure first» держится не на памяти, а на одной команде. Гоняй её
перед любым pack, демо или внешним обещанием:

```bash
bash scripts/gate.sh            # ~30 s, локально, без GPU и без Commercial
bash scripts/gate.sh --verbose  # плюс вывод шагов, которые прошли
PYTHON=python3.11 bash scripts/gate.sh   # другой интерпретатор
```

| # | Шаг | Что доказывает |
|---|---|---|
| 1 | sandbox unit tests | `pytest -m "not integration"` — ядро песочницы цело |
| 2 | sandbox examples | каждый `sandbox/examples/*/project.toml` отрабатывает (`cli run` даёт non-zero при `budget_ok=false`) |
| 3 | demo pack | `sandbox/scripts/demo_pack.sh` — домены D0–D4, то, что видит инвестор |
| 4 | doc links | относительные ссылки в `docs/**`, `AGENTS.md`, `STATUS.md`, `README.md` ведут в живые файлы |
| 5 | eval scorer | `scripts/score_agent_eval.py --selftest`, иначе smoke интерфейса |
| 6 | root tests | `pytest tests -q` |

Правила чтения вывода:

- каждый шаг — своя строка `OK` / `FAIL` / `SKIP` + время;
- последняя строка одна: `GATE: PASS` или `GATE: FAIL`, exit code следует за ней;
- **`FAIL` печатает вывод упавшего шага целиком** — не надо перезапускать руками;
- шлюз не останавливается на первом провале: сначала полная картина, потом вердикт;
- `SKIP` (нет `tests/` или нет скорера) **не** красит шлюз в красный: отсутствие
  чужого артефакта — не поломка. Но и не считается проверкой.

Проверку ссылок можно гонять отдельно, она мгновенная:

```bash
python3 scripts/check_doc_links.py                 # дефолтный набор документов
python3 scripts/check_doc_links.py -v docs/X.md    # конкретный файл
```

Якоря (`FILE.md#section`) **не** валидируются — проверяется только файловая
часть. Иначе каждое переименование заголовка красило бы CI.

---

## 10. CI (GitHub Actions)

`.github/workflows/ci.yml` — на `push` и `pull_request`, `ubuntu-latest`,
Python **3.11 и 3.12** (3.11 — минимум из `sandbox/pyproject.toml`, 3.12 — то,
что стоит на лабораторной машине; чтобы они не разъехались молча).

CI повторяет шаги 1, 2, 4, 6 шлюза плюс проверку, что в индекс не попали веса
(`*.gguf`, `*.safetensors`, `*.ckpt`, `*.pt`, `*.pth`).

Чего в CI **нет** и почему — прежде чем «чинить» красный или недостающий шаг:

| Не в CI | Причина |
|---|---|
| 3 integration-теста (`-m integration`) | поднимают Outpost: release-бинарь `sovereignd` + GGUF + Metal. На чистом раннере этого нет — добавить значит либо красный CI, либо фальшивый pass |
| train / LoRA / export | GPU и веса; лаборатория, не раннер |
| Synapse Gate smoke | Commercial бинарь и порт `:8097` |

Отсюда практическое следствие: **зелёный CI ≠ пройденный шлюз**. Integration
и всё, что трогает GGUF, гоняются локально:

```bash
cd sandbox && PYTHONPATH=src python -m pytest -q -m integration
```
