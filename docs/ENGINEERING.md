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

- [ ] `.gguf` не в индексе
- [ ] Скрипты executable + `set -euo pipefail`
- [ ] Docs ссылки не битые (относительные пути)
- [ ] STATUS обновлён
- [ ] Одна логическая тема на commit
