# Eval

`prompts.ru.jsonl` — стартовый набор. Считать baseline на **базовой** модели (до LoRA), потом на Proto.

Agent formats (Cursor-like, model-side only): `prompts/agent-v0.jsonl` + `agent-rubric.md` → `results/agent-v0-hammer2-baseline.md`.

---

## agent-v0: собрать → оценить → прочитать разброс

### 1. Собрать ответы

Поднять `sovereignd` с нужным конфигом (`config/sovereign.agent-*.toml`, порт `:8097`), затем:

```bash
python3 scripts/run_agent_eval.py --model outpost-tiny-hammer --out eval/results/raw/agent-v0-<tag>/
```

Дефолт сэмплинга — **greedy (`--temperature 0.0`)**, не 0.2. При 0.2 один и тот же
прогон давал ±1 балл, и решения «+1 / −1» принимались по шуму.

### 2. Оценить

```bash
python3 scripts/score_agent_eval.py eval/results/raw/agent-v0-<tag>/
```

Пишет `score.json` в каталог прогона и печатает markdown-таблицу.
Скорер детерминированный, только stdlib, сети не требует — работает на записанных
ответах, поэтому старый прогон можно переоценить в любой момент.

Семь id проверяются машинно (`tool_json`, `tool_json_args`, `schema_extract`,
`router_hint`, `budget_sentences`, `plan_steps`, `plan_tool_mix`).
Три семантических (`code_lite`, `refuse_public`, `self_check`) получают эвристику
и всегда помечены `needs_human: true` — их число это черновик для человека, а не измерение.
У `plan_steps` машинно проверяется только формат: содержательный пункт рубрики
(air-gap + `/health`) выводится отдельным `content_axis` и остаётся за человеком.

### 3. Повторы и разброс

```bash
python3 scripts/run_agent_eval.py --repeats 5 --out eval/results/raw/agent-v0-<tag>/ && python3 scripts/score_agent_eval.py eval/results/raw/agent-v0-<tag>/
```

При `--repeats N > 1` каждая строка `all.jsonl` несёт поле `repeat`, а скорер
докладывает так же, как `closed-sandbox stress`:

```text
- score mean±stdev: **19.333 ± 0.577** / 20
- score range: `19` … `20`
- unstable across repeats: `budget_sentences`, `plan_tool_mix`
```

Как читать: **дельта меньше stdev — это не улучшение модели.** Сравнивать прогоны
можно только если разница между mean больше разброса; `unstable_ids` показывает,
какие именно промпты «плавают» и портят сумму.

### 4. Тесты скорера

```bash
python -m pytest tests -q
```

---

## Что лежит в git

Промпт-сеты, `all.jsonl`, `meta.json`, `score.json` каждого прогона — в git:
без них цифру в CARD/STATUS нечем перепроверить. Per-prompt дампы `<id>.txt`
остаются вне git (тот же контент, что и в `all.jsonl`, только россыпью).
Веса — никогда.
