# Synapse E5 → Closed Sandbox (import)

Frozen KPIs from Synapse `export/e5-brain-escalate` CARD (2026-07-29).

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli run examples/synapse_e5_import/project.toml
```

Does **not** execute torch inside sandbox. Refresh fixture from a live Synapse bench:

```bash
cd ~/Projects/synapse && .venv/bin/python export/e5-brain-escalate/bench.py
cd ~/Projects/neurolab && python3 sandbox/scripts/export_synapse_e5_fixture.py
cd sandbox && PYTHONPATH=src python -m closed_sandbox.cli run examples/synapse_e5_import/project.toml
```

Report: `../../reports/e5-live-export-2026-07-29.md`.
