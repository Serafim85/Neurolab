# Closed Sandbox UI (ported)

> **CS-P01** Overview · **P02** Editor · **P03** Run · **P04** Diff · **P05** Ask · NL-ADR-018

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli ui
# → http://127.0.0.1:8765/         CS-P01 Overview
# → http://127.0.0.1:8765/editor   CS-P02 Editor
# → http://127.0.0.1:8765/run      CS-P03 Run
# → http://127.0.0.1:8765/diff     CS-P04 Diff
# → http://127.0.0.1:8765/ask      CS-P05 Ask
```

| Piece | Role |
|---|---|
| `overview.html` | CS-P01 project list |
| `editor.html` | CS-P02 manifest validate/save |
| `run.html` / `diff.html` / `ask.html` | P03–P05 |
| `ui_server.py` | Stdlib HTTP APIs |

Studio mocks + parity under Commercial `design/sandbox/`.
