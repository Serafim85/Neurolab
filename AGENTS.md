# AGENTS.md — правила для AI agents (Нейролаб)

> **Читай этот файл первым** в каждой сессии в `neurolab`.  
> Живой статус: `STATUS.md` · Архитектура: `docs/ARCHITECTURE.md` · Решения: `docs/DECISIONS.md`

---

## 1. Миссия

**Нейролаб** — инженерная лаборатория **своих весов** для продукта **Outpost** (commercial: `~/Projects/AI-Platform-Vision`).

Мы не продаём пилотам «сырой training lab». Мы готовим **воспроизводимый supply chain моделей**:

```text
данные → adapt (LoRA/SFT) → GGUF + паспорт → smoke в Outpost → pack
```

**Девизы:** надёжность и качество.  
**Экономика:** при минимальных ресурсах (compute, RAM, время, люди) — максимум измеримого результата.  
**North star:** перекрыть сильные стороны frontier **своей системой** (линейка + Synapse + контур) с измеримой экономией ресурсов — не клон Kimi/Grok (`docs/STRATEGY.md` · NL-ADR-019).  
Investor excerpt: `docs/INVESTOR-NORTH-STAR.md` · build: `docs/NORTH-STAR-BUILD.md`.

**Фильтр любой задачи:**

> Это повышает качество / надёжность / допустимость весов для контура Outpost при разумной цене?  
> Да → делай. Нет → backlog в `STATUS.md`, не кодь.

---

## 2. Что это / что это не

| Это | Это не |
|---|---|
| Model R&D: cards, eval, train scripts, packs | Commercial runtime (`sovereignd`) |
| Tiny + micro-MoE suite (dense эксперты) | Training foundation 70B с нуля (пока) |
| Lab / internal | Пилот-оффер и GTM-обещания |
| Export в GGUF для Outpost | Свой matmul / свой inference stack |

Commercial остаётся единственным местом пилотного кода. Сюда — только модели и документация вокруг них.

---

## 3. Карта документов (читай по роли)

| Файл | Зачем |
|---|---|
| **`AGENTS.md`** | этот файл — ритуал и запреты |
| **`STATUS.md`** | Done / In progress / Backlog / Session log |
| **`docs/ARCHITECTURE.md`** | архитектура сети и системы Lab→Outpost |
| **`docs/CONSTRUCT.md`** | гибкий конструкт слотов + профили железа (NL-ADR-006) |
| **`docs/INTELLECTUAL-CANON.md`** | интеллектуальный канон линейки (книги, papers, lab notes) |
| **`docs/CONTOUR-EGRESS.md`** | контур / своё облако / публичный LLM default off |
| **`docs/SYNAPSE-BRIDGE.md`** | pointer → Synapse Brain bridge |
| **`docs/COMMERCIAL-GATE-HANDOFF.md`** | Outpost Gate: explain consumer + audit (impl in Commercial) |
| **`docs/PILOT-CONTOUR-CHAT.md`** | pilot contour chat: hammer2 + guard 20/20, smoke, demo |
| **`docs/CLOSED-SANDBOX-MVP.md`** | Closed Sandbox: SNN studio в контуре (`sandbox/`) |
| **`docs/CLOSED-SANDBOX-AGENTS.md`** | вход для агентов sandbox (ритуал + карта канонов) |
| **`docs/CLOSED-SANDBOX-CANON.md`** | научный канон SNN/neuromorphic |
| **`docs/CLOSED-SANDBOX-CODE.md`** | канон кода sandbox (plugins, DoD) |
| **`docs/CLOSED-SANDBOX-UI.md`** | канон UI (научный/промышленный UX) |
| **`docs/CLOSED-SANDBOX-UI-PIPELINE.md`** | Design Studio → ★ → Port (Closed Sandbox) |
| **`docs/CLOSED-SANDBOX-UI-REQS.md`** | FR экранов UI + трассировка к макетам |
| **`docs/CLOSED-SANDBOX-INDUSTRY.md`** | индустриальный канон (buyers, стандарты) |
| **`docs/CLOSED-SANDBOX-GRANTS.md`** | грантовая карта Closed Sandbox (EIC / Chips JU / Innosuisse) |
| **`docs/CLOSED-SANDBOX-VERIFY.md`** | верификация pytest ask↔Outpost |
| **`docs/TRAIN-TINY-LORA.md`** | рецепт LoRA → GGUF |
| **`construct/example.toml`** | schema манифеста микросетей |
| **`docs/GOALS.md`** | цели, задачи, use-cases моделей |
| **`docs/INTEGRATION.md`** | куда и как встраиваем в Outpost |
| **`docs/SCALE-PLAN.md`** | план масштабирования Tiny→Mid→Large / suite |
| **`docs/ENGINEERING.md`** | подход, code style, логи, DoD |
| **`docs/DECISIONS.md`** | ADR лаборатории |
| **`docs/STRATEGY.md`** | краткая стратегия треков A/B |
| **`docs/MICRO-MOE.md`** | suite мини-экспертов (product MoE) |
| `models/*/CARD.md` | паспорт каждой модели |
| `eval/` | промпты, рубрика, results |
| Commercial `docs/MODEL-SOVEREIGNTY-PATH.md` | канон лестницы для продукта (ADR-018/045/046) |

---

## 4. Ритуал сессии

### Старт

1. Прочитать **`STATUS.md`** — не дублировать сделанное.
2. Прочитать **`docs/DECISIONS.md`** — не переоткрывать принятое.
3. Сверить **`docs/ARCHITECTURE.md`** § Current focus — одна задача.
4. При arch/train выборе — глянуть **`docs/INTELLECTUAL-CANON.md`** §2–3.  
   Для Closed Sandbox — старт с **`docs/CLOSED-SANDBOX-AGENTS.md`** (наука / код / индустрия).
5. Взять **одну** работу из In progress или top Backlog.

### Во время

- Минимальный diff; документация и код — на одном уровне важности.
- Любой эксперимент → запись в Session log + обновление CARD / results.
- Веса и большие датасеты **не** в git (см. `.gitignore`).
- Не обещать в Commercial GTM то, чего нет в `STATUS.md` Done.

### Конец (обязательно)

1. Обновить `STATUS.md`:
   - Done / In progress / Backlog
   - **Session log** (2–8 строк): что сделано, как проверить, следующие шаги
2. Новое архитектурное решение → ADR в `docs/DECISIONS.md`.
3. **Закоммитить и запушить.** Сессия не закрыта, пока `git status` не чист
   и `git push` не прошёл.

```bash
git status --short          # ничего лишнего? весов и секретов нет?
git add -A && git commit -m "…"
git push
```

Пункт 3 появился не просто так: однажды ритуал требовал только `STATUS.md`,
и три недели работы — вся платформа Closed Sandbox — три недели пролежали
незакоммиченными в репозитории без remote. Девиз «надёжность» начинается здесь.

---

## 5. Принципы разработки

Полностью: `docs/ENGINEERING.md`.

Кратко:

1. **Measure first** — baseline / eval до и после adapt.
2. **One lever** — одна переменная за итерацию (данные *или* rank *или* base).
3. **Dense first** — не arch-MoE на старте; micro-MoE = отдельные GGUF + router.
4. **Construct-first evolution** — новая способность = слот + skills/profile (`docs/CONSTRUCT.md`), не форк «одной сети».
5. **Canon-backed choices** — arch/train/scale решения опираются на `docs/INTELLECTUAL-CANON.md` (cite adopt/defer).
6. **Ship as GGUF** — нет успеха без загрузки в Outpost.
7. **Passport** — LICENSE, SHA, base, дата в CARD.
8. **Min resource / max result** — LoRA и 3B до 14B; profile `lite` на слабом железе.
9. **Reliability & quality** — скрипты + rubric; autotune только с audit и lock after boot.

---

## 6. Текущий фокус (синхронизировать со STATUS)

| Сейчас | Не сейчас |
|---|---|
| Outpost-Tiny на базе Qwen2.5-3B; LoRA data / adapt | Mid 7–14B, Large, arch-MoE |
| Construct schema v0.1 (манифест); runtime load — Gate B+ | Полный online auto-NAS / mid-request swap |
| Eval harness + качество vs baseline 14/16 | Пять экспертов suite сразу |
| Документация и инженерный контур Lab | Обучение на ПДн заказчика |
---

## 7. Граница с Commercial

| Действие | Где |
|---|---|
| Train / LoRA / export GGUF / eval моделей | **neurolab** |
| Runtime, API, UI, pilot bundle | **AI-Platform-Vision** |
| Роутинг экспертов в проде | Commercial Gate B (`agents.toml` / ModelPool) |
| Баг runtime | Commercial first |

Пути по умолчанию:

```text
Commercial binaries: ~/Projects/AI-Platform-Vision/target/release/{sovereign,sovereignd}
Lab config:          ./config/sovereign.baseline.toml  (port 8090)
Base GGUF:           ./artifacts/base/*.gguf
```

---

## 8. Anti-patterns (запрещено)

- Training PR / pipeline в commercial repo без human + ADR
- Arch-MoE / pretrain с нуля «потому что круто»
- Коммит `.gguf`, сырых корпусов, секретов
- Несколько новых экспертов suite в одной сессии
- Заявление «отечественная 70B» без паспорта и eval
- Пропуск baseline / rubric «потом замерим»
- Ломать воспроизводимость скриптов ради разового notebook

---

## 9. Когда спросить human

- Смена locked base (не Qwen2.5-3B) для Tiny v0
- Бюджет GPU / платный cloud train
- Данные с риском ПДн / NDA
- Merge pack в Commercial / GTM wording
- Переход на Mid / Large / arch-MoE

**Не спрашивать** для: docs, eval sheet, CARD updates, скриптов smoke, STATUS.

---

*Нейролаб · надёжность и качество · min resources → max result*
