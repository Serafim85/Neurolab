# Studio ★ review — CS-L03 → CS-P03 (first Port slice)

> **★ 2026-08-02** · **Ported 2026-08-02** (NL-ADR-018)  
> Live UI: `cd ~/Projects/neurolab/sandbox && PYTHONPATH=src python -m closed_sandbox.cli ui` → http://127.0.0.1:8765/  
> Studio mock: [CS-P03](http://127.0.0.1:9394/design/sandbox/CS-P03-run-results.html)  
> Parity: Commercial `design/sandbox/parity/CS-P03.yaml` (ported · 9/10 done, 1 waived — cancel)

## Ported artifacts

| Artifact | Path |
|---|---|
| UI | `neurolab/sandbox/ui/run.html` |
| Server | `neurolab/sandbox/src/closed_sandbox/ui_server.py` |
| CLI | `closed-sandbox ui` |
| ★ mock | Commercial `design/sandbox/CS-P03-run-results.html` |

## Waivers

- **Cancel** — sync engine  
- **Per-scenario metrics** — `metrics.by_scenario` (snn_lif conditions); UI/report (2026-08-04)

## Next screens

Other Lab CS-L* need separate ★ before Port.
