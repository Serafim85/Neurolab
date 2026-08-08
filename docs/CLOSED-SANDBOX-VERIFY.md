# Closed Sandbox — verification sheet

> **Last verified:** 2026-07-28 (host Mac, human + agent)  
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

Example D0 metrics (seed 42, typical): F1 ~0.9, `budget_ok=true`, spike_count ≫ 100.

---

## 3. What is covered

| Check | Where |
|---|---|
| Manifest validate / load example | `tests/test_manifest.py` |
| D0 LIF run + F1/budget + diff | `tests/test_snn_lif.py` |
| Report write / CLI run+diff | `tests/test_cli_report.py` |
| Ask errors (disabled / bad provider / missing public key / unreachable) | `tests/test_contour_ask_unit.py` |
| Ask ↔ live Outpost (API) | `tests/test_ask_outpost.py` |
| Ask ↔ live Outpost (CLI) | `tests/test_ask_cli.py` |
| Outpost boot fixture | `tests/conftest.py` + `outpost_util.py` |

---

## 4. v0.1 DoD

See MVP §9. Ask/Outpost and unit engines marked done after 2026-07-28 verification.
