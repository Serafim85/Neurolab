# Studio ★ review — CS-P05 Ask

> **Status:** ★ + **Ported** 2026-08-04  
> Parity: Commercial `design/sandbox/parity/CS-P05.yaml`  
> Production: neurolab `sandbox/ui/ask.html` · `closed-sandbox ui` → `/ask`

## Scope

FR-UI-030 Ask + FR-UI-031 contour honesty (public risk banner cannot hide).

## Accept

- [x] Human ★ (session develop track Ask)
- [x] Port UI + `/api/ask` (CLI `contour_ask.ask`)
- [x] Provider toggle local|public with mandatory public banner
- [x] pytest `test_ui_cs_p05.py`

## Notes

- Live Outpost / public key required for real answers; UI surfaces AskError clearly.
- Default provider from `project.toml` `[contour]`; UI override is ephemeral (not written back).
