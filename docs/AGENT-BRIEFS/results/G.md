# Result G — One source of truth + STATUS rotation

**Brief:** [`G-docs-single-truth.md`](../G-docs-single-truth.md) · **Date:** 2026-08-08
**Git:** ничего не коммитил / не пушил (волна 2, мержит оркестратор).

---

## 1. `STATUS.md` — было / стало

| | Было | Стало |
|---|---|---|
| Строк | **449** | **248** |
| Записей журнала | 59 | **28** (27 августовских + 1 новая G) |
| Записей в архиве | — | **32** (`docs/SESSIONS-2026-07.md`, 232 строки) |

Бриф считал 423 строки / 58 записей — файл подрос после аудита, до старта G он был
449 строк. Потери информации нет: перенесённый хвост сверен построчно
(`difflib.unified_diff` STATUS-хвост vs архив → **0 различий**, 221 строка).

---

## 2. Найденные расхождения (9, из них 3 были в брифе)

| № | Где | Что врало | Статус |
|---|---|---|---|
| 1 | `AGENTS.md` §6 | «Outpost-Tiny … LoRA data / adapt» как текущий фокус — противоречит `STATUS.md` «Pause Tiny LoRA sheet chase» | **исправлено** → указатель на STATUS |
| 2 | `AGENTS.md` §6 | «качество vs baseline **14/16**» — шкала /16 мертва, актуальная /20 | **исправлено** (цифра убрана) |
| 3 | `docs/ARCHITECTURE.md` §6 | «Tiny baseline + LoRA на 3B» / «Mid/Large — после Tiny quality bar» как «сейчас делаем» | **исправлено** → указатель на STATUS |
| 4 | `AGENTS.md` §4 Старт шаг 3 | ритуал отправлял за фокусом в устаревший `ARCHITECTURE.md` §Current focus | **исправлено** → `STATUS.md` §Summary + §Next |
| 5 | `docs/CLOSED-SANDBOX-VERIFY.md` | «Last verified 2026-07-28», unit «11 passed» при фактических 51 | **исправлено** (новая строка + освежён §3 covered) |
| 6 | `docs/CLOSED-SANDBOX-MVP.md` §9 | «Verified 2026-07-28: unit 11 passed» | **исправлено** (добавлен блок 2026-08-08, старый оставлен как история) |
| 7 | `AGENTS.md` §4 Конец шаг 1 + §3 карта + `docs/INDEX.md` | требовали обновлять в STATUS секции **«Done / In progress / Backlog»**, которых в `STATUS.md` нет (там Summary / Ladder / Next / Session log) — агент физически не мог выполнить ритуал как написано | **исправлено** |
| 8 | `docs/CLOSED-SANDBOX-MVP.md` §3 + шапка | «Status: draft for coding (2026-07-26)»; в таблице §3 «Объект проектирования — **ещё нет**», «Sandbox core — **ещё нет**» при работающих D0–D4 + UI P01–P05 и 51 тесте | **исправлено** (минимально: статусы) |
| 9 | `STATUS.md` §Next п.3 | пункт «Refresh stale sheets … make AGENTS §6 / ARCHITECTURE §6 point at this file» — это и есть трек G | **снят** из §Next, ушёл в Session log |

### Расхождения вне владения брифа G (не правил — нужно решение / чужой трек)

| Где | Что | Кому |
|---|---|---|
| `README.md:38` | «Сейчас: **Track A baseline accepted (14/16)** → подготовка LoRA» — **четвёртое** место с текущим фокусом, и оно тоже врёт (мёртвая шкала + Tiny LoRA на паузе) | оркестратор / human. Предлагаю: `Сейчас: см. [STATUS](STATUS.md) §Summary + §Next.` |
| `docs/SCALE-PLAN.md:36,49-51` | «L3 Outpost-Tiny ← **мы здесь**», Phase N0 `- [x] baseline 14/16` + незакрытые `- [ ] LoRA data` / `- [ ] Tiny-v0/v1 adapt → re-eval` при «Pause Tiny LoRA» | оркестратор. Чекбокс 14/16 — история, оставить; «мы здесь» и открытые пункты стоит пометить `paused (STATUS §Next)` |
| `sandbox/README.md:67` | `# unit — expect 11 passed` — тот же отставший счёт | **бриф F** (владелец `sandbox/`) → `expect 51 passed` |
| `docs/DECISIONS.md:28`, `eval/RUBRIC.md:29`, `eval/results/tiny-v{0,1}-vs-baseline.md` | 14/16 как **исторический** результат на 8 промптах | трогать не нужно — это история, не «текущее» |

---

## 3. Фактические числа тестов

```bash
cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"
# 51 passed, 3 deselected in 12.78s
```

- Вписал **51 passed, 3 deselected** (дата 2026-08-08) в VERIFY §2 и MVP §9.
- **Integration не запускал.** Набор (3 теста) требует Metal/GPU host + Commercial
  release `sovereignd` + GGUF hammer2; агент работает в sandbox-окружении Cursor.
  В листах записано «not run» с указанием требований и последнего зелёного
  прогона (2026-07-28, 3 passed) — число не выдумано.
- Разбивка (`--collect-only`): by_scenario 7 · neuro_chip 6 · ui_p05 5 ·
  hybrid/contour_ask/biosignal по 4 · ui_p03/snn_lif/manifest/cli_report/biocompute
  по 3 · ui_p04/ui_p01_p02/synapse_import по 2 = 51.
- Прогон шёл **одновременно с треком F** (правит `sandbox/src` + `sandbox/tests`).
  Расхождения с ожидаемым нет — получил ровно 51, как в аудите; но если F добавит
  тесты, строку VERIFY нужно будет обновить его числом. Оговорка про параллельность
  вписана в VERIFY §2. Контрольный повторный прогон в конце сессии — снова 51.
- Ссылки после правок проверены `python3 scripts/check_doc_links.py` (появился у
  трека I): 53 файла, 140 относительных ссылок → **OK**.

---

## 4. Строка в STATUS Session log

Впи́сана мной (я владелец `STATUS.md`), оркестратору мержить не нужно:

```markdown
### 2026-08-08 — One source of truth + STATUS rotation (brief G)

- Фокус больше не дублируется: `AGENTS.md` §6 и `ARCHITECTURE.md` §6 — указатели
  на этот файл; мёртвая шкала `14/16` из §6 убрана (актуальная — `/20`)
- Ритуал `AGENTS.md` §4 «Старт» шаг 3 теперь ведёт в `STATUS.md` §Summary + §Next,
  а не в устаревший `ARCHITECTURE.md` §6; требование коммита в «Конец» не тронуто
- Листы верификации освежены: VERIFY + MVP §9 → **51 passed** (`not integration`,
  3 deselected) на 2026-08-08; integration не прогонялся (нужен Metal/GPU host +
  Commercial release `sovereignd`) — так и записано, число не выдумано
- Ротация журнала: 32 записи ≤2026-07-31 → `docs/SESSIONS-2026-07.md` (verbatim,
  diff = 0); STATUS **449 → 248 строк**; INDEX + Cursor rule обновлены
- Verify: `cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"`
  → **51 passed, 3 deselected**; в VERIFY §2 появилась строка 2026-08-08,
  прежние «11 passed» остались только как история прогонов
- Остаётся вне брифа G: `README.md` §Треки и `docs/SCALE-PLAN.md` §3 всё ещё
  объявляют «сейчас» Track A / baseline 14/16, `sandbox/README.md` — «expect 11 passed»
```

---

## 5. Изменённые файлы

| Файл | Что |
|---|---|
| `STATUS.md` | шапка: «единственный источник фокуса»; §Next п.3 снят + перенумерация; журнал обрезан до 2026-08-01 + указатель на архив; новая запись G |
| `docs/SESSIONS-2026-07.md` | **новый** — 32 записи ≤2026-07-31 verbatim + шапка «здесь не редактируем» |
| `AGENTS.md` | §6 → указатель (без цифр); шапка; §3 карта (STATUS + архив); §4 Старт 3/5 и Конец 1 — под реальную структуру STATUS. **Пункт 3 «Закоммитить и запушить» и абзац про три недели без коммита — не тронуты** |
| `docs/ARCHITECTURE.md` | §6 «Current focus vs future topology» → «Current focus → STATUS», таблица заменена на указатель + принцип лестницы |
| `docs/CLOSED-SANDBOX-VERIFY.md` | шапка Last verified; §2 две строки 2026-08-08 + оговорка про параллельный трек F; §3 covered дополнен D1–D4 / by_scenario / UI P01–P05 / synapse_import |
| `docs/CLOSED-SANDBOX-MVP.md` | §9 блок Verified 2026-08-08 + ссылка на VERIFY; шапка Status; §3 «ещё нет» → «есть» |
| `docs/INDEX.md` | STATUS = источник фокуса; **новая строка** `SESSIONS-2026-07.md`; AGENT-BRIEFS — волны 1 и 2 |
| `.cursor/rules/00-neurolab.mdc` | правило 5 → фокус только из STATUS. **Правило 12 (clean git status + push) не тронуто** |

Не трогал: `docs/DECISIONS.md`, `sandbox/`, `eval/`, `scripts/`, `.gitignore`,
`.github/`, `models/`, `docs/CLAIMS.md`, `README.md`, `docs/SCALE-PLAN.md`.

INDEX-строк из результатов других треков волны 2 забрать не смог — на момент
работы в `docs/AGENT-BRIEFS/results/` лежали только `A–D` (волна 1). Домержит
оркестратор.

---

## 6. Требует решения человека

1. **`README.md` §Треки** — единственное оставшееся место, где «сейчас» объявлено
   в обход STATUS (Track A / 14/16). Файл вне владения G. Правка — одна строка.
2. **`docs/SCALE-PLAN.md`** — «мы здесь» на L3 и открытые чекбоксы LoRA против
   «Pause Tiny LoRA sheet chase». Нужно решить: пометить `paused` или снять паузу.
3. **Правило ротации журнала** зафиксировано только в `AGENTS.md` §4 Конец
   («записи старше текущего месяца → `docs/SESSIONS-<YYYY-MM>.md`»). Если хотите
   это как ADR — предлагаю **NL-ADR-025 «STATUS = single source of focus + monthly
   session-log rotation»**: фокус живёт только в `STATUS.md`; `AGENTS.md` §6 /
   `ARCHITECTURE.md` §6 — указатели; журнал старше текущего месяца выносится в
   `docs/SESSIONS-<YYYY-MM>.md` без правки текста. ADR вставляет оркестратор.
4. **Integration-прогон** (3 теста) — нужен человек на Mac с Metal/GPU и собранным
   Commercial `sovereignd`, чтобы строка VERIFY 2026-08-08 закрылась полностью.
