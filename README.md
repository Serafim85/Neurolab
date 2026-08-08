# Нейролаб (neurolab)

Инженерная лаборатория **своих весов** для [Outpost](https://outpost-llm.com)  
Commercial runtime: `~/Projects/AI-Platform-Vision`

**Девизы:** надёжность · качество · минимум ресурсов → максимум результата.

---

## Агентам: начни здесь

1. **[`AGENTS.md`](AGENTS.md)** — правила сессии  
2. **[`STATUS.md`](STATUS.md)** — что в работе  
3. **[`docs/INDEX.md`](docs/INDEX.md)** — полная карта docs  

| Doc | Тема |
|---|---|
| [ARCHITECTURE](docs/ARCHITECTURE.md) | архитектура сети и системы |
| [CONSTRUCT](docs/CONSTRUCT.md) | **гибкий конструкт** слотов + автоподстройка к железу |
| [INTELLECTUAL-CANON](docs/INTELLECTUAL-CANON.md) | книги, статьи, Anthropic/OpenAI, векторы будущего |
| [CONTOUR-EGRESS](docs/CONTOUR-EGRESS.md) | своё облако клиента · публичный LLM default off |
| [TRAIN-TINY-LORA](docs/TRAIN-TINY-LORA.md) | LoRA → GGUF recipe |
| [GOALS](docs/GOALS.md) | цели и задачи |
| [INTEGRATION](docs/INTEGRATION.md) | встраивание в Outpost |
| [SCALE-PLAN](docs/SCALE-PLAN.md) | масштабирование |
| [ENGINEERING](docs/ENGINEERING.md) | стиль, логи, DoD |
| [MICRO-MOE](docs/MICRO-MOE.md) | suite мини-экспертов |

---

## Треки

| | |
|---|---|
| **A — Outpost-Tiny** | dense chat на Qwen2.5-3B → LoRA → GGUF |
| **B — Micro-MoE suite** | extract / summarize / router как отдельные GGUF |

Текущий фокус и актуальные цифры — **только** в [`STATUS.md`](STATUS.md)
(§Summary + §Next). Здесь их намеренно нет: дублирование однажды уже привело
к четырём расходящимся описаниям «сейчас».

---

## Quick start (baseline)

```bash
./scripts/pull_base.sh   # if GGUF missing
# terminal 2:
#   ~/Projects/AI-Platform-Vision/target/release/sovereignd \
#     ~/Projects/neurolab/config/sovereign.baseline.toml
./scripts/run_baseline.sh
# score → eval/results/baseline-qwen25-3b.md
```

Веса в git не кладём (`.gitignore`).
