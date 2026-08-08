# chip-fpga-lite-v0 — named FPGA target (`fpga_snn_lite_v0`)

Still an **estimate** (NL-ADR-021): LUT/BRAM/DSP proxies + `out/chip_export.json` hook.
No Vivado/Quartus/bitstream.

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli run examples/chip_fpga_lite_v0/project.toml
# → out/metrics.json + out/chip_export.json
```

| Key | Role |
|---|---|
| `chip_target` | `fpga_snn_lite_v0` |
| `chip_luts_est` / `chip_bram18_est` / `chip_dsp_est` | fabric proxies |
| `chip_export` | machine-readable hook for later vendor map (human) |
