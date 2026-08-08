# Demo pack — Closed Sandbox + Gate (≈10 min)

> **Status:** ready (2026-08-03)  
> **SOW language:** [`SYNAPSE-GATE-SOW-WORDING.md`](SYNAPSE-GATE-SOW-WORDING.md) (**Approved**)  
> **Audience:** investor / partner / internal — not clinical, not fab

---

## 0. Prep (once)

```bash
# Lab
cd ~/Projects/neurolab/sandbox
pip install -e ".[dev]"   # or PYTHONPATH=src

# Optional Gate (Commercial + GGUF)
#   GGUF: ~/Projects/neurolab/artifacts/outpost-tiny-hammer.Q4_K_M.gguf
#   cd ~/Projects/AI-Platform-Vision
#   CARGO_TARGET_DIR=$PWD/target cargo build -p sovereign-daemon --release
```

---

## 1. Script (10 minutes)

| Min | Show | Command / URL | Say (Approved wording) |
|---|---|---|---|
| 0–1 | Hook | — | Split breed: Synapse decides; Outpost explains + audits; LLM does not fix class |
| 1–4 | Domains D0–D4 | `bash scripts/demo_pack.sh` | One studio core; silicon + bio **digital** domains; economy via budget_ok |
| 4–6 | Run UI | `PYTHONPATH=src python -m closed_sandbox.cli ui` → http://127.0.0.1:8765/ | CS-P03 Port: same metrics as CLI |
| 6–9 | Gate | start `sovereignd` + smoke | Escalate → explain → audit; flag off by default |
| 9–10 | Close | — | Out of scope: fab, wet-lab, Synapse-chat, LLM-as-class-fixer |

### Domains one-liner each

| ID | Example | One line |
|---|---|---|
| D0 | `anomaly_v0` | LIF SNN anomaly |
| D1 | `chip_estimate_v0` / `chip_fpga_lite_v0` | Chip/FPGA **estimate** + export hook (not bitstream) |
| D2 | `biocompute_grn_v0` | Digital GRN toy (not wet-lab) |
| D3 | `biosignal_ecg_v0` | Synthetic ECG → spikes (not clinical) |
| D4 | `hybrid_ecg_snn_v0` | Bio front → silicon SNN composition |

---

## 2. Fast verify (domains only, ~30–60s)

```bash
cd ~/Projects/neurolab/sandbox
bash scripts/demo_pack.sh
# expect: 6 pass / 0 fail
```

---

## 3. UI (CS-P03)

```bash
cd ~/Projects/neurolab/sandbox
PYTHONPATH=src python -m closed_sandbox.cli ui
# → http://127.0.0.1:8765/  · Run on examples/anomaly_v0/project.toml
```

---

## 4. Synapse Gate (optional, needs GGUF)

```bash
cd ~/Projects/AI-Platform-Vision
./target/release/sovereignd config/sovereign.synapse-gate.toml   # :8097
./scripts/synapse-gate-smoke.sh                                  # 3/3 roles
```

Talking point (Approved):

> Outpost принимает escalate от Synapse, объясняет на локальном GGUF и пишет audit; class на escalate — Synapse specialist, не LLM.

---

## 5. Leave-behind links

| Doc | Role |
|---|---|
| This file | Demo runbook |
| `SYNAPSE-GATE-SOW-WORDING.md` | Allowed / forbidden claims |
| `CLOSED-SANDBOX-MVP.md` | Domain map D0–D4 |
| Commercial ADR-054 | Gate engineering |

---

## 6. DoD

- [x] `demo_pack.sh` green (6 domains)  
- [x] UI start documented  
- [x] Gate smoke documented  
- [x] Wording tied to Approved SOW doc  
