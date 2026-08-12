# Brief L — Generalize `stress` CLI + UI columns off spikes

**Track:** Последняя жёсткая привязка к спайкам в CLI/UI  
**Primary repo:** `/Users/valentin/Projects/neurolab`  
**Read first:** `docs/CLOSED-SANDBOX-CODE.md` §3 · NL-ADR-025 in `DECISIONS.md` · `sandbox/src/closed_sandbox/cli.py` (`_cmd_stress`) · `sandbox/ui/`  
**Wave:** 3 · **model preference:** cheap–mid · **Slot:** 2 (после J)  
**Owns:** `sandbox/src/closed_sandbox/cli.py`, `sandbox/ui/**`, `sandbox/tests/test_*stress*` (создать при необходимости)

---

## Проблема

```python
f1s = [float(r["f1"]) for r in rows]          # KeyError on generic
spikes = [float(r["spike_count"]) for r in rows]
```

UI (`app.js`, `run.html`, `overview.html`) хардкодит спайковые колонки — не падает,
но generic показывает прочерки.

---

## Do exactly

1. Summary/`stress` берут primary из `metric_primary` + значение; spike/f1 колонки
   — только если ключи есть в metrics.
2. Флаг `--min-mean-f1`: либо deprecate + warning + alias на `--min-primary`, либо
   оставить как alias. Не ломать существующих вызывающих без warning.
3. UI: колонки из фактически вернувшихся ключей (как report после F).
4. Тест: stress (или unit, эмулирующий summary) на fixture/`biocompute` без KeyError.
5. `bash scripts/gate.sh` → PASS.

---

## Do not

- Менять engine envelope (уже NL-ADR-025).
- `git commit`.
- React/production UI вне `sandbox/ui`.

---

## Result file

`docs/AGENT-BRIEFS/results/L.md` — решение по флагу, verify, leftover.
