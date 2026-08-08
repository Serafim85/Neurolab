# Brief I — CI + одна команда «measure first»

**Track:** Превратить девиз в исполняемый шлюз, а не в ритуал на память
**Primary repo:** `/Users/valentin/Projects/neurolab`
**Read first:** `AGENTS.md` §5 · `docs/ENGINEERING.md` · `docs/DEMO-PACK-SANDBOX.md` · `sandbox/scripts/demo_pack.sh`
**Wave:** 2026-08-08 (E–I) · orchestrator merges STATUS/ADR/INDEX

---

## Зачем этот бриф

Девиз №1 лаборатории — **measure first**, но проверка держится на памяти: CI нет,
lock-файла в git нет, LICENSE нет. Unit-набор песочницы идёт **13 секунд** и не
требует GPU — то есть автоматизировать его ничего не стоит, и не сделано это
только потому, что не дошли руки.

Репозиторий только что получил remote: `git@github.com:Serafim85/Neurolab.git`.

---

## Do exactly

### 1. `.github/workflows/ci.yml`

На `push` и `pull_request`. Обязательно **без GPU и без Commercial бинарей** —
только то, что честно проходит на чистом раннере:

- Python 3.11+
- быстрый набор песочницы: `cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"` (сейчас 51 passed)
- прогон всех примеров: каждый `sandbox/examples/*/project.toml` через `closed_sandbox.cli run` должен отработать
- корневой набор `python -m pytest tests -q`, **если** каталог `tests/` существует (его создаёт бриф E — сделай шаг необязательным, а не падающим)
- проверка битых внутренних ссылок в markdown: все относительные ссылки из `docs/**/*.md`, `AGENTS.md`, `STATUS.md`, `README.md` ведут в существующие файлы

Integration-тесты (3, требуют Metal + Commercial release) в CI **не** включать —
явно отметить это комментарием в workflow, чтобы никто не «починил» их добавлением.

Проверку ссылок реализуй скриптом (`scripts/check_doc_links.py`, stdlib), чтобы её
можно было запускать локально, а не только в CI. Учти якоря вида `FILE.md#section`
— проверяй существование файла, якоря можно не валидировать (напиши это в выводе).

### 2. `scripts/gate.sh` — один шлюз

Одна команда перед любым pack / демо / внешним обещанием. Печатает одну итоговую
строку `GATE: PASS` / `GATE: FAIL` и ненулевой код при провале.

Состав шагов:

1. unit-набор песочницы
2. все примеры прогоняются
3. `sandbox/scripts/demo_pack.sh` (сейчас 6 pass / 0 fail) — **вызывай, не правь**
4. проверка ссылок в документах
5. скорер eval, **если** `scripts/score_agent_eval.py` существует (бриф E) — иначе `SKIP` с явной строкой

Каждый шаг — своя строка `OK` / `FAIL` / `SKIP`, чтобы было видно, что именно
отвалилось. Не прячь вывод упавшего шага.

### 3. Воспроизводимость

- `LICENSE` — **не выбирай сам.** Лаборатория частная, лицензия это решение
  человека. Вместо файла напиши в результате вопрос человеку с 2–3 вариантами и
  их последствиями
- lock-файл: `requirements-train.lock` раньше стоял в `.gitignore` (уже убрано),
  но самого файла на диске нет. Не генерируй его вслепую на этой машине —
  опиши в результате, как его собрать и чем это полезно
- Секция в `docs/ENGINEERING.md`: как запускать шлюз локально и что делает CI

---

## Твои файлы (не выходи за них)

```text
.github/workflows/ci.yml       scripts/gate.sh
scripts/check_doc_links.py     docs/ENGINEERING.md
```

Читать можно всё. **Писать — только в этот список.**

---

## Forbidden

- Любые `git` команды: add / commit / push. Мержит оркестратор
- Править `STATUS.md`, `docs/DECISIONS.md`, `docs/INDEX.md`, `AGENTS.md` — бриф G / оркестратор
- Трогать `sandbox/**` (включая `demo_pack.sh` и тесты) — это бриф F
- Трогать `eval/`, `.gitignore`, `scripts/run_agent_eval.py`, `scripts/score_agent_eval.py` — это бриф E
- Трогать `models/`, `docs/CLAIMS.md` — это бриф H
- Добавлять в CI шаги, требующие GPU, Metal, сети к моделям или Commercial бинарей
- Создавать `LICENSE` без решения человека
- Делать CI зелёным за счёт `|| true` и пропуска реальных проверок

---

## Definition of Done

- [ ] CI-workflow проходит логически на чистом раннере (проверь шаги локально)
- [ ] `bash scripts/gate.sh` работает и печатает одну итоговую строку
- [ ] Проверка ссылок находит реальные битые ссылки, если они есть — доложи найденные
- [ ] Отсутствие `tests/` и `score_agent_eval.py` даёт `SKIP`, а не `FAIL`
- [ ] `docs/AGENT-BRIEFS/results/I.md` написан

---

## Result file → `docs/AGENT-BRIEFS/results/I.md`

Обязательно включи:

1. Вывод `scripts/gate.sh` целиком, как он выглядит сейчас
2. Все найденные битые ссылки в документах (это побочная, но ценная находка)
3. Вопрос человеку про LICENSE с вариантами
4. **Предложенную строку в STATUS Session log** и строку в `docs/INDEX.md`, если нужна
5. Список изменённых файлов
