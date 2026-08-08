# Closed Sandbox — verification sheet

> **Last verified:** 2026-08-08 (unit, agent) · integration — 2026-07-28 (host Mac)  
> **Product:** [`CLOSED-SANDBOX-MVP.md`](CLOSED-SANDBOX-MVP.md) · code: `sandbox/`

---

## 1. Commands

```bash
cd /Users/valentin/Projects/neurolab/sandbox

# Unit (no Outpost)
PYTHONPATH=src pytest -m "not integration" -q

# Integration (boots sovereignd + hammer2 on :8098)
PYTHONPATH=src:tests pytest -m integration -v

# Manual smoke
bash scripts/run_ask_outpost_smoke.sh
```

**Needs for integration:**  
- GGUF `artifacts/outpost-tiny-hammer.Q4_K_M.gguf`  
- Commercial `~/Projects/AI-Platform-Vision/target/release/sovereignd`  
- Config `config/sovereign.sandbox-ask.toml`  
- Metal/GPU host (not restricted CI sandbox without GPU)

Wrong cwd (e.g. `AI-Platform-Vision`) will collect unrelated tests — always `cd neurolab/sandbox`.

---

## 2. Results log

| Date | Suite | Result | Notes |
|---|---|---|---|
| 2026-07-28 | `not integration` | **11 passed** | manifest, snn_lif, CLI/report, ask unit errors |
| 2026-07-28 | `integration` (agent) | **3 passed** | ask API ×2 + CLI ask |
| 2026-07-28 | full suite (human, Mac) | **11 + 3 passed** | confirmed in terminal after VERIFY expand |
| 2026-08-08 | `not integration` (agent) | **51 passed, 3 deselected** | D0–D4 + by_scenario + UI P01–P05 + synapse_import + ask unit |
| 2026-08-08 | `integration` | **not run** | needs Metal/GPU host + Commercial release `sovereignd`; last green 2026-07-28 |

Строка 2026-08-08 закрывает 11-дневный отрыв листа: между 07-28 и 08-08 добавились
D1–D4, by_scenario и UI-экраны, а лист продолжал утверждать «11 passed».
Прогон шёл параллельно с брифом F (правки `sandbox/src` + `sandbox/tests`) —
число зафиксировано на момент прогона.

Example D0 metrics (seed 42, typical): F1 ~0.9, `budget_ok=true`, spike_count ≫ 100.

---

## 3. What is covered

| Check | Where |
|---|---|
| Manifest validate / load example | `tests/test_manifest.py` |
| D0 LIF run + F1/budget + diff | `tests/test_snn_lif.py` |
| D1 neuro_chip estimate + FPGA target | `tests/test_neuro_chip.py` |
| D2 biocompute (boolean GRN) | `tests/test_biocompute.py` |
| D3 biosignal (synthetic ECG/EEG) | `tests/test_biosignal.py` |
| D4 hybrid (front → snn_lif backend) | `tests/test_hybrid.py` |
| Synapse E5 fixture import | `tests/test_synapse_import.py` |
| `by_scenario` split / stub across domains | `tests/test_by_scenario_domains.py` |
| UI screens CS-P01…P05 | `tests/test_ui_cs_p01_p02.py` · `test_ui_cs_p03.py` · `test_ui_cs_p04.py` · `test_ui_cs_p05.py` |
| Report write / CLI run+diff | `tests/test_cli_report.py` |
| Ask errors (disabled / bad provider / missing public key / unreachable) | `tests/test_contour_ask_unit.py` |
| Ask ↔ live Outpost (API) | `tests/test_ask_outpost.py` |
| Ask ↔ live Outpost (CLI) | `tests/test_ask_cli.py` |
| Outpost boot fixture | `tests/conftest.py` + `outpost_util.py` |

---

## 4. v0.1 DoD

See MVP §9. Ask/Outpost and unit engines marked done after 2026-07-28 verification.
