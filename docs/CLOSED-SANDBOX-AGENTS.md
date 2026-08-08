# Closed Sandbox — карта документов для агентов

> **Зачем:** один вход: что читать до кода / до смены архитектуры / до грантовой формулировки.  
> **Код:** `sandbox/` · **ADR:** 010–015

---

## 1. Три опоры (обязательный минимум)

| Опора | Документ | Вопрос |
|---|---|---|
| **Продукт** | [`CLOSED-SANDBOX-MVP.md`](CLOSED-SANDBOX-MVP.md) | *Что* строим, DoD, non-goals, домены |
| **Наука** | [`CLOSED-SANDBOX-CANON.md`](CLOSED-SANDBOX-CANON.md) | *Почему* LIF/SNN; adopt/defer papers |
| **Код** | [`CLOSED-SANDBOX-CODE.md`](CLOSED-SANDBOX-CODE.md) | *Как* писать поддерживаемо и масштабируемо |
| **UI** | [`CLOSED-SANDBOX-UI.md`](CLOSED-SANDBOX-UI.md) | *Как выглядит* инструмент (научный/промышленный UX) |
| **UI pipeline** | [`CLOSED-SANDBOX-UI-PIPELINE.md`](CLOSED-SANDBOX-UI-PIPELINE.md) | *Как* Design Studio → ★ → Port |
| **UI FR** | [`CLOSED-SANDBOX-UI-REQS.md`](CLOSED-SANDBOX-UI-REQS.md) | *Какие* экраны / accept criteria |
| **Индустрия** | [`CLOSED-SANDBOX-INDUSTRY.md`](CLOSED-SANDBOX-INDUSTRY.md) | *Для кого* / стандарты / конкуренты / стык bio↔silicon |
| **Деньги** | [`CLOSED-SANDBOX-GRANTS.md`](CLOSED-SANDBOX-GRANTS.md) | *Куда* за грантами (после демо) |
| **Verify** | [`CLOSED-SANDBOX-VERIFY.md`](CLOSED-SANDBOX-VERIFY.md) | Результаты pytest / ask↔Outpost |

Общий Lab: `AGENTS.md` · `ENGINEERING.md` · `STATUS.md` · `DECISIONS.md`.  
Outpost LLM (hammer2): `INTELLECTUAL-CANON.md` — **не** смешивать с SNN-каноном.

---

## 2. Ритуал сессии (Closed Sandbox)

1. `STATUS.md` — не дублировать.  
2. `CLOSED-SANDBOX-MVP.md` §2–4 — один домен за сессию (v0 = D0).  
3. Если трогаешь нейрон/метрики/kind → `CLOSED-SANDBOX-CANON.md` adopt/defer.  
4. Если пишешь/рефакторишь код → `CLOSED-SANDBOX-CODE.md` + `ENGINEERING.md` §3.  
5. Если UI / plots / IA → `CLOSED-SANDBOX-UI.md` + **PIPELINE** + **FR**; код UI только после ★.  
6. Если pitch / buyer / стандарт / конкурент → `CLOSED-SANDBOX-INDUSTRY.md`.  
7. Конец: STATUS Session log; новый `domain` → ADR.

**Одна задача за сессию.** Не открывать D2 biocompute, пока D0 не зелёный по DoD.

---

## 3. Когда какой канон

| Ситуация | Читать |
|---|---|
| Новый CLI / plugin / тест | CODE + MVP architecture |
| Web UI / графики / layout | **UI** + **PIPELINE** + **FR** + MVP |
| Новый макет / Port UI | PIPELINE §4–5; без ★ — только Lab в Design Studio |
| Смена LIF → Liquid / HH | CANON + ADR |
| «Сделаем как ChatGPT / Notion» | **UI** (скорее anti-pattern) + INDUSTRY |
| Bio / бактерии / органоиды | CANON §3b + INDUSTRY bio adjacency; wet-lab = out |
| Заявка на грант | GRANTS + INDUSTRY narrative + демо-метрики |
| `ask` / contour / public LLM | MVP §8 + `CONTOUR-EGRESS.md` |

---

## 4. Принцип качества (для агентов)

Код без канонов = хрупкий прототип.  
Канон без метрик = эссе.  
Индустрия без продукта = слайды.

**Формула:** MVP × наука × индустрия × код × UI → измеримый `sandbox/` артефакт.
