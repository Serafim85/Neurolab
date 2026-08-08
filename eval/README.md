# Eval

`prompts.ru.jsonl` — стартовый набор. Считать baseline на **базовой** модели (до LoRA), потом на Proto.

Agent formats (Cursor-like, model-side only): `prompts/agent-v0.jsonl` + `agent-rubric.md` → `results/agent-v0-hammer2-baseline.md`.

Пока без автоматического scorer: таблица в `STATUS.md` или `eval/results/` (gitok JSON, не веса).
