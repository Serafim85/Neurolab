# Closed Sandbox — lab prototype

Closed-contour **multi-domain** sandbox: silicon SNN *and later* biotech compute models.

```text
manifest → run → metrics → report → ask
```

**Domains:** `snn_lif` · `neuro_chip` · `biocompute` · `biosignal` · `hybrid` · `synapse_import`.

**Docs:** [`CLOSED-SANDBOX-AGENTS.md`](../docs/CLOSED-SANDBOX-AGENTS.md) · [`CLOSED-SANDBOX-VERIFY.md`](../docs/CLOSED-SANDBOX-VERIFY.md)  
**ADR:** NL-ADR-010 … 014

## Demo pack (10 min)

```bash
bash scripts/demo_pack.sh          # D0–D4 · expect 6 pass
# runbook: ../docs/DEMO-PACK-SANDBOX.md
```

## Quick start

```bash
PYTHONPATH=src python -m closed_sandbox.cli run examples/anomaly_v0/project.toml
PYTHONPATH=src python -m closed_sandbox.cli diff \
  examples/anomaly_v0/out/metrics.json examples/anomaly_v0/out/metrics.json

# Seed sweep + report (lab stress)
PYTHONPATH=src python -m closed_sandbox.cli stress examples/anomaly_v0/project.toml \
  --n-seeds 20 --out reports/stress-anomaly-v0

# CS-P03 Run+Results UI (NL-ADR-018)
PYTHONPATH=src python -m closed_sandbox.cli ui
# → http://127.0.0.1:8765/       CS-P03 Run
# → http://127.0.0.1:8765/diff   CS-P04 Diff

# D1 neuro_chip rough estimate
PYTHONPATH=src python -m closed_sandbox.cli run examples/chip_estimate_v0/project.toml
# FPGA named target + chip_export.json
PYTHONPATH=src python -m closed_sandbox.cli run examples/chip_fpga_lite_v0/project.toml

# D2 digital biocompute GRN toy
PYTHONPATH=src python -m closed_sandbox.cli run examples/biocompute_grn_v0/project.toml

# D3 synthetic ECG biosignal
PYTHONPATH=src python -m closed_sandbox.cli run examples/biosignal_ecg_v0/project.toml

# D4 hybrid: ECG front → SNN backend
PYTHONPATH=src python -m closed_sandbox.cli run examples/hybrid_ecg_snn_v0/project.toml
```

Latest stress note: [`reports/anomaly-v0-stress-2026-07-29.md`](reports/anomaly-v0-stress-2026-07-29.md) · speed+import: [`reports/anomaly-v0-speed-synapse-import-2026-07-29.md`](reports/anomaly-v0-speed-synapse-import-2026-07-29.md)

Import Synapse E5 KPIs (no torch):

```bash
PYTHONPATH=src python -m closed_sandbox.cli run examples/synapse_e5_import/project.toml
# refresh fixture from live Synapse E5 bench:
#   synapse: .venv/bin/python export/e5-brain-escalate/bench.py
#   neurolab: python3 sandbox/scripts/export_synapse_e5_fixture.py
# reports: reports/e5-live-export-2026-07-29.md · reports/e5-ask-2026-07-29.md
```

## Tests

```bash
# unit — expect 11 passed
PYTHONPATH=src:tests pytest -m "not integration" -q

# integration (Outpost + hammer2 on :8098) — expect 3 passed
PYTHONPATH=src:tests pytest -m integration -v

# manual smoke
bash scripts/run_ask_outpost_smoke.sh
```

Always run from `neurolab/sandbox` (not `AI-Platform-Vision`).

Assistant (`ask`): **default local Outpost**; **opt-in public LLM** via `[contour] provider = "public"`.
