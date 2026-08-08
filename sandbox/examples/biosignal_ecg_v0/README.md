# biosignal-ecg-v0 — D3 biosignal

Synthetic ECG-like trace → threshold spike encode → small LIF classifier.
**Not** a medical device (NL-ADR-023).

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli run examples/biosignal_ecg_v0/project.toml
```

Also available: `[signal].kind = "synthetic_eeg_v0"`.

D2 (`biocompute`) v0.1 is **closed**; richer GRN kinds are backlog.
