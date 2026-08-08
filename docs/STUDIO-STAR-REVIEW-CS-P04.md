# Studio ★ review — CS-P04 Diff

> **Status:** ★ + **Ported** 2026-08-04  
> Parity: Commercial `design/sandbox/parity/CS-P04.yaml` (6 done · 1 waived — nested by_scenario table)  
> Production: neurolab `sandbox/ui/diff.html` · `closed-sandbox ui` → `/diff`

## Scope

FR-UI-020 — Diff two `metrics.json` files; `n_changed` + deltas match CLI.

## Accept

- [x] Human ★ (session 2026-08-04 — develop track #1)
- [x] Port UI + `/api/diff`
- [x] Parity yaml
- [x] pytest `test_ui_cs_p04.py`

## Notes

- Nested `by_scenario` skipped in HTML table (full object still in API/CLI).
- Paths restricted under sandbox root (same policy as Run).
