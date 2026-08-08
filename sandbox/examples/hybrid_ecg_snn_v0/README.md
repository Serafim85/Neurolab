# hybrid-ecg-snn-v0 — D4 hybrid

Pipeline: **synthetic ECG front** (D3-style) → **threshold encode** → **SNN LIF backend** (D0-style).

Digital composition only (NL-ADR-024). Not clinical / not wet-lab.

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli run examples/hybrid_ecg_snn_v0/project.toml
```

Metrics highlight: `hybrid_pipeline`, `hybrid_front`, `hybrid_backend`.
