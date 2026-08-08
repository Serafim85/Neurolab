# Closed Sandbox — канон кода (для агентов)

> **Статус:** living (2026-07-28) · NL-ADR-013  
> **Наследует:** `ENGINEERING.md` (стиль Lab)  
> **Продукт:** `CLOSED-SANDBOX-MVP.md` · пакет: `sandbox/`  
> **Цель:** код **понятный, читаемый, поддерживаемый, масштабируемый** (domain plugins), без god-object и без premature fab/bio.

---

## 1. Девизы кода

1. **Measure first** — нет merge без теста + metrics JSON на example.  
2. **One domain per change** — v0 только `snn_lif`; новый domain = новый пакет + ADR.  
3. **Thin core, fat plugins** — core не знает LIF-формул; plugin не знает CLI.  
4. **English identifiers** — docs могут быть RU; код/API/тесты — EN.  
5. **Min resource** — stdlib + мало зависимостей; тяжёлые libs только с причиной в PR/STATUS.  
6. **No secrets** — API keys только env; никогда в `project.toml` / git.

---

## 2. Слои (обязательная граница)

```text
CLI / API / local UI (`ui_server`)
    → engine.dispatch(domain)
        → domains/<id>/  (sim, encode, train hooks)
    → report (common schema)
    → contour_ask (local | public)
```

| Слой | Можно | Нельзя |
|---|---|---|
| `manifest.py` | validate TOML, defaults | считать spikes |
| `engine.py` | load plugin, run scenarios | хардкод LIF |
| `domains/snn_lif/` | нейроны, датасет, domain metrics | HTTP к LLM |
| `report.py` | md/json/diff | импорт конкретного domain |
| `contour_ask.py` | OpenAI-compatible client | менять веса сети |
| `ui_server.py` | serve CS-P* · POST run · export | LIF / domain formulas |

Нарушение границы = рефактор до merge.

---

## 3. Контракт domain plugin

Каждый `domains/<id>/` обязан экспортировать (имена стабильные):

```python
# conceptual contract — implement in code
DOMAIN_ID: str  # e.g. "snn_lif"

def validate_project(project: dict) -> None: ...
def run(project: dict, *, seed: int) -> dict:
    """Return metrics dict; must include metric_primary + budget_ok."""
```

Правила:

- `run` **чист** от сети/LLM (кроме чтения локальных fixture paths).  
- Возврат: JSON-serializable dict.  
- Обязательные ключи (D0): `f1` или `accuracy`, `spike_count`, `synops`, `latency_proxy_ms`, `budget_ok`.  
- Domain-specific ключи — с префиксом (`bio_`, `chip_`) later.  
- Падение: явный exception с *что сделать*; не silent NaN.

Новый domain = копия контракта + `examples/<name>/` + тесты.

---

## 4. Стиль Python (`sandbox/`)

| Правило | Деталь |
|---|---|
| Version | 3.11+ |
| Types | type hints на публичном API |
| Packaging | `src/closed_sandbox/`; `pyproject.toml` |
| Format | ruff/black-compatible; 1 style на репо |
| Tests | `pytest`; smoke на `examples/anomaly_v0` |
| Config | TOML манифесты; без YAML-зоопарка в v0 |
| Logging | stdlib `logging`; уровень INFO для CLI |
| Random | все стохастические пути принимают `seed` |

Запрещено в v0:

- глобальные синглтоны состояния сети;  
- `import *`;  
- скачивание датасетов в runtime без явной команды;  
- зависимость от GPU для D0 example;  
- копипаст LIF в `engine.py`.

---

## 5. Именование

| Что | Как |
|---|---|
| Пакет | `closed_sandbox` |
| Domain dirs | `snn_lif`, `biocompute`, `biosignal`, `neuro_chip` |
| CLI | `closed-sandbox` (console_script) |
| Example ids | `anomaly-v0` |
| Metrics keys | `snake_case`, стабильные навсегда |
| Тесты | `test_<module>.py` |

---

## 6. Definition of Done (любой PR в `sandbox/`)

- [ ] Тест(ы) зелёные локально  
- [ ] Example `run` пишет metrics JSON  
- [ ] Нет секретов / больших бинарников в git  
- [ ] Публичные функции с type hints  
- [ ] Границы слоёв соблюдены  
- [ ] Если новый domain/kind — ADR + строка в CANON/INDUSTRY  
- [ ] `STATUS.md` Session log (кратко)

---

## 7. Масштабирование кода (как не сломать)

| Этап | Код |
|---|---|
| v0–v1 | plugins D0–D4 + `synapse_import` · hybrid = composition |
| v1 | второй plugin; общий metrics envelope |
| v2 | hybrid pipeline = composition of plugins, не монолит |

Правило трёх: третий копипаст helper → вынести в `closed_sandbox/util/`.  
Не вводить DI-фреймворки / microservices в Lab prototype.

---

## 8. Связь с наукой и индустрией

- Формула нейрона / метрика energy → сначала **CANON** (adopt), потом код.  
- «Сделаем как конкурент X» → **INDUSTRY**, потом минимальный plugin, не rewrite core.  
- Нет paper → нет нового `kind` в merge.

---

## 9. Анти-паттерны

- «Пока захардкодим, потом разнесём» для domain logic в CLI  
- Тянуть PyTorch+JAX+Brian2 сразу «на вырост»  
- Био-симулятор полного клеточного метаболизма в v0  
- Публичный LLM без `provider=public` и env key  
- Документация только в чате, без STATUS
