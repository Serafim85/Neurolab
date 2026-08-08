# biocompute-grn-v0 — D2 digital biocompute

Toy **boolean gene-regulatory network** (sim only). No wet-lab (NL-ADR-022).

**Status:** D2 v0.1 **complete** (2026-08-03).

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli run examples/biocompute_grn_v0/project.toml
```

| Metric | Meaning |
|---|---|
| `accuracy` / `f1` | holdout on majority-of-inputs task |
| `bio_n_genes` / `bio_n_edges` | circuit size |
| `bio_resource_proxy` | sim ops (not ATP Joules) |
| `spike_count` | always 0 (not SNN) |
