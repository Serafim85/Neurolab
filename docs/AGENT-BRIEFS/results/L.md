# Brief L — result

**Track:** Generalize `stress` CLI + UI columns off spikes  
**Date:** 2026-08-13  
**Repo:** `/Users/valentin/Projects/neurolab`

---

## 1. Flag decision

**`--min-mean-f1` → deprecate + alias `--min-primary`**

- New canonical flag: `--min-primary` (default `0.75`).
- `--min-mean-f1` kept as alias; emits `warning: --min-mean-f1 is deprecated; use --min-primary` on stderr via custom argparse action.
- Exit gate unchanged: code `3` when primary mean &lt; threshold.

---

## 2. What changed

| File | Change |
|---|---|
| `sandbox/src/closed_sandbox/cli.py` | `_cmd_stress` driven by `metric_primary`; optional f1/spike/accuracy means only when keys present; dynamic per-seed table columns; `--min-primary` + deprecated `--min-mean-f1` alias |
| `sandbox/ui/app.js` | Metric cards + scenario table columns from returned keys (like `report.py`) |
| `sandbox/ui/run.html` | Placeholder metrics/scenario head — filled by JS |
| `sandbox/ui/overview.html` | Dynamic metric header |
| `sandbox/ui/overview.js` | Metric columns derived from `/api/projects` row data |
| `sandbox/tests/test_stress_generic.py` | **new** — fixture `cost_probe_test`, biocompute, deprecated flag |

---

## 3. Verification

| Check | Result |
|---|---|
| `bash scripts/gate.sh` | **PASS** (88 sandbox tests, 6 steps) |
| `test_stress_generic_fixture` | no KeyError; summary uses `fit_score_mean` |
| `test_stress_biocompute` | no KeyError; primary `accuracy` |
| `test_stress_min_mean_f1_alias` | deprecation warning + exit 0 on anomaly_v0 |
| `test_cli_stress_small` (existing) | still passes |

---

## 4. Leftovers

1. **`ui_server.py` `_list_projects`** still exposes fixed fields (`f1`, `accuracy`, `spike_count`) — overview JS scans those; domains with only `fit_score`/`chip_fit_score` show sparse columns until API is generalized (out of scope).
2. **`stress` summary** may still include optional means (e.g. `f1_mean`) when the domain reports those keys even if not primary — by design per brief (“only if keys exist”).
3. No git commit (per brief).
