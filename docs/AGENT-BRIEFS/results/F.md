# Brief F — result

**Track:** Generalize the sandbox metrics envelope + golden tests
**Date:** 2026-08-08
**Repo:** `/Users/valentin/Projects/neurolab`
**Wave:** 2 (E–I) · orchestrator merges STATUS / ADR / INDEX

---

## 1. SNN strictness — how it is solved and why

**Mechanism:** an optional module-level constant in the domain plugin.

```python
DOMAIN_ID = "snn_lif"
METRICS_FAMILY = "snn"      # absent ⇒ "generic"
```

`engine.metrics_family(plugin)` reads it, defaults to `generic`, and raises
`EngineError` on an unknown value (typo protection at plugin load, before `run`).

| Family | Core owes | Extra |
|---|---|---|
| `generic` (default) | `metric_primary` (str) · numeric value under that name · `budget_ok` (bool) | — |
| `snn` | same | `spike_count` · `synops` · (`f1` or `accuracy`) |

**Declared families (by fact, checked in code):**

| Domain | Family | Why |
|---|---|---|
| `snn_lif` (D0) | `snn` | spiking simulator |
| `neuro_chip` (D1) | `snn` | estimate is driven by spike/synop activity |
| `biosignal` (D3) | `snn` | threshold encode → LIF |
| `hybrid` (D4) | `snn` | LIF backend |
| `biocompute` (D2) | `generic` | not a spiking domain — `spike_count = 0` **by design** (NL-ADR-022, and `contour_ask` states it as a canonical fact). Demanding a spike budget from it was always a lie the core got away with because 0 is present. |
| `synapse_import` | `generic` | host wrapper, not a simulator. Its strictness did not disappear: `_REQUIRED_SOURCE = ("accuracy", "spike_count", "synops")` still rejects a source fixture without those keys, i.e. the check now lives in the layer that actually knows the contract (`CLOSED-SANDBOX-CODE.md` §2: thin core / fat plugins). Locked by `test_synapse_import_keeps_source_strictness`. |

**Why a plugin constant and not a manifest field:** the family is a property of
the *implementation*, not of a user-editable project. A manifest flag would let
a pilot silently relax D0 by editing TOML; a constant cannot be relaxed without
touching the plugin, which is a reviewed change. It also costs nothing for
existing plugins (default = `generic`), and `_load_plugin` validates it, so a
typo like `METRICS_FAMILY = "spiking"` fails loudly instead of silently
degrading D0 to the loose envelope.

Both directions are locked by tests: `test_shipped_snn_domains_declare_snn_family`
/ `test_non_spiking_domains_declare_generic_family` fail if someone flips a
family by accident, and `test_snn_family_still_requires_spikes` /
`test_snn_family_still_requires_f1_or_accuracy` prove the old strictness is
byte-for-byte intact for the SNN family.

---

## 2. What changed

### Envelope (`engine.py`)

Old: `required = ("spike_count", "synops", "budget_ok")` + `f1|accuracy` for
**every** domain. New: `CORE_REQUIRED_KEYS = ("metric_primary", "budget_ok")`,
plus a numeric value under `metric_primary`, plus the family extras above.

Also normalizes numpy scalars (`np.float64` / `np.bool_`) into Python values via
`.item()` so metrics stay JSON-serializable without importing numpy in the core.

Verified by fact, not memory: all six shipped domains already return
`metric_primary` (`snn_lif`, `biocompute`, `biosignal`, `hybrid` from
`[task].metric_primary` with a default; `neuro_chip` defaults to
`chip_fit_score`; `synapse_import` to `accuracy`), so nothing had to be added to
any domain to satisfy the new core requirement.

### Economy (`manifest.py` → `engine.py` → `report.py`)

```toml
[economy]
cost_key = "chip_power_mw"   # any numeric metrics key
cost_unit = "mW"             # optional, display only
```

`manifest.validate_project` defaults `[economy]` to `{}` and rejects a
non-string / empty `cost_key` and a non-string `cost_unit`. `engine` copies it
into metrics as `economy_cost_key` / `economy_cost_unit` (report/diff only see
metrics, never the project). `report.enrich_economy` then adds
`quality_per_unit_cost = metric_primary / cost_key`.

Existing proxies untouched: `quality_per_kspike` and `quality_per_ksynop` keep
their names and their formulas (`1000 * quality / max(cost, 1)`).

Live demo wired into `examples/chip_estimate_v0/project.toml`
(`cost_key = "chip_power_mw"`), so the feature ships in a real artifact and not
only in tests.

### Report (`report.py`)

- Summary bullets are emitted **only for keys the domain returned** — a
  non-spiking domain no longer gets `- spike_count (avg): n/a`.
- Economy block lists only the proxies that exist; when there are none it says
  `no cost proxy for this domain — declare [economy] cost_key …` instead of
  printing `n/a`.
- `## Per scenario` columns are the union of keys the rows actually have,
  ordered: `n` → primary metric → cost key → house order → the rest
  alphabetically → `budget_ok` last.
- `ensure_by_scenario` stub rows now also carry the declared cost key.

For `anomaly_v0` the rendered report is **identical to the pre-change output**
(same bullets, same `| scenario | n | f1 | accuracy | spike_count | synops |`).
`chip_estimate_v0` gains real columns where it previously had none.

### Deliberate behaviour change (flagging it explicitly)

`quality_per_kspike` / `quality_per_ksynop` are no longer emitted when
`spike_count` / `synops` is `0`. Before, `synapse_import` reported
`quality_per_kspike = 863.6` with zero spikes — a number a customer could cite
that means nothing (`1000 * accuracy / max(0, 1)`). Keys are **not** renamed and
values for any domain with real spikes are bit-identical; the proxy simply
disappears where there is no cost to divide by, consistent with the new
`cost_key` rule. Locked by `test_zero_cost_gets_no_ratio` and
`test_spike_proxies_unchanged_for_snn`.

### Golden files

`sandbox/tests/golden/` next to the tests:

| File | Role |
|---|---|
| `anomaly_v0_metrics_seed42.json` / `…seed43.json` | frozen `run_project` output, `wall_ms` pinned to `0.0` (only volatile field) |
| `anomaly_v0_report.md` | byte-exact `report.md` |
| `anomaly_v0_diff.json` | byte-exact `diff` output through the real CLI path (`write_json` → `load_metrics_json` → `diff_metrics`) |
| `cost_probe_report.md` | byte-exact report for a **non-spiking** domain |

Live runs are covered without making the suite hostage to numpy/BLAS
differences: `test_live_run_keeps_golden_shape` compares the *structure* of a
real `anomaly_v0` run against the golden (headings, bullet labels, table column
layout), and `test_live_run_keeps_golden_metric_keys` compares the metric key
set. Numbers may move; format and schema may not.

Regeneration after an intentional format change is a documented one-liner:

```bash
cd sandbox && PYTHONPATH=src:tests python tests/test_report_golden.py
```

Verified: regeneration is deterministic (two runs byte-identical), and the
goldens genuinely bite — appending one line to `anomaly_v0_report.md` fails
both `test_report_md_is_byte_exact` and `test_live_run_keeps_golden_shape`.

### Test-only domain plugin

`sandbox/tests/fixture_domains.py` (not in `domains/` — a shipped domain needs
its own ADR). `cost_probe_test` is a deterministic non-spiking cost estimator:
no `spike_count`, no `synops`, no `f1`/`accuracy`, `metric_primary = fit_score`,
cost key `unit_cost_eur`. Registered through the `register_domain` fixture in
`conftest.py`, which inserts the module into `sys.modules` under
`closed_sandbox.domains.<id>` (monkeypatched, auto-removed) — `_load_plugin`
resolves it via `importlib.import_module`, which returns an existing
`sys.modules` entry as-is. Seven more one-rule-violation plugins cover the error
paths.

---

## 3. Verification

| Check | Before | After |
|---|---|---|
| `cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"` | **51 passed**, 3 deselected | **85 passed**, 3 deselected |
| `sandbox/examples/*/project.toml` через `closed_sandbox.cli run` | 7/7 exit 0 | 7/7 exit 0 |

All seven examples (`anomaly_v0`, `biocompute_grn_v0`, `biosignal_ecg_v0`,
`chip_estimate_v0`, `chip_fpga_lite_v0`, `hybrid_ecg_snn_v0`,
`synapse_e5_import`) were run before **and** after the change; every one exits 0
and writes `metrics.json` + `report.md`. No test was deleted, renamed, or
weakened; +34 are new.

```bash
cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"
cd /Users/valentin/Projects/neurolab && for p in sandbox/examples/*/project.toml; do \
  PYTHONPATH=sandbox/src python -m closed_sandbox.cli run "$p" >/dev/null || echo "FAIL $p"; done
```

---

## 4. Files changed

| File | Change |
|---|---|
| `sandbox/src/closed_sandbox/engine.py` | envelope: `METRICS_FAMILIES`, `metrics_family()`, `_check_envelope`, `_attach_economy`, numpy-scalar normalization; family validated at plugin load |
| `sandbox/src/closed_sandbox/report.py` | `enrich_economy` generic `cost_key`; zero-cost guard; `write_markdown` split into `_header_lines` / `_economy_lines` / `_scenario_columns` / `_scenario_lines`; stub row carries cost key |
| `sandbox/src/closed_sandbox/manifest.py` | `[economy]` default + validation of `cost_key` / `cost_unit` |
| `sandbox/src/closed_sandbox/domains/snn_lif/__init__.py` | `METRICS_FAMILY = "snn"` |
| `sandbox/src/closed_sandbox/domains/neuro_chip/__init__.py` | `METRICS_FAMILY = "snn"` |
| `sandbox/src/closed_sandbox/domains/biosignal/__init__.py` | `METRICS_FAMILY = "snn"` |
| `sandbox/src/closed_sandbox/domains/hybrid/__init__.py` | `METRICS_FAMILY = "snn"` |
| `sandbox/src/closed_sandbox/domains/biocompute/__init__.py` | `METRICS_FAMILY = "generic"` + why |
| `sandbox/src/closed_sandbox/domains/synapse_import/__init__.py` | `METRICS_FAMILY = "generic"` + note that strictness lives in `_REQUIRED_SOURCE` |
| `sandbox/examples/chip_estimate_v0/project.toml` | `[economy] cost_key = "chip_power_mw"`, `cost_unit = "mW"` |
| `sandbox/tests/conftest.py` | **new fixture** `register_domain` |
| `sandbox/tests/fixture_domains.py` | **new** — test-only plugins (non-spiking + 7 broken) |
| `sandbox/tests/test_metrics_envelope.py` | **new** — 28 tests: families, non-spiking run, envelope errors, `[economy]`, manifest validation |
| `sandbox/tests/test_report_golden.py` | **new** — 6 golden tests + regeneration entry point |
| `sandbox/tests/golden/anomaly_v0_metrics_seed42.json` | **new** — frozen input |
| `sandbox/tests/golden/anomaly_v0_metrics_seed43.json` | **new** — frozen input |
| `sandbox/tests/golden/anomaly_v0_report.md` | **new** — golden report |
| `sandbox/tests/golden/anomaly_v0_diff.json` | **new** — golden diff |
| `sandbox/tests/golden/cost_probe_report.md` | **new** — golden report, non-spiking domain |

Untouched by contract: `ui_server.py`, `sandbox/ui/`, `cli.py`, `eval/`,
`scripts/`, `.gitignore`, `STATUS.md`, `docs/**`, `models/`. No git command was
run — the orchestrator commits.

---

## 5. Needs a decision / another track

1. **`cli.py stress` is still spike-only** (not my file set). `_cmd_stress`
   indexes `r["f1"]`, `r["accuracy"]`, `r["spike_count"]` and hardcodes the
   per-seed table, so `closed-sandbox stress` would `KeyError` on a truly
   non-spiking domain. Harmless today (every shipped domain still emits those
   keys) but it is the last hard spike dependency in the core CLI. Suggested
   follow-up: drive the stress summary off `metric_primary` the same way
   `report.py` now does.
2. **UI still assumes spike columns** (`sandbox/ui/` is another track).
   `app.js` and `run.html` hardcode the `f1 / accuracy / spike_count / synops`
   scenario table, and `overview.html` a `spike_count` column; a non-spiking
   domain would render `—`. Nothing breaks today. Suggested follow-up: build the
   scenario table from the row keys, exactly as `_scenario_columns` does, and
   surface `quality_per_unit_cost` with its `economy_cost_unit` label.
3. **Docs need one line each** (owned by G / orchestrator, not written here):
   - `docs/CLOSED-SANDBOX-CODE.md` §3 still lists the D0 required keys as
     `f1|accuracy, spike_count, synops, latency_proxy_ms, budget_ok` — should
     become the core envelope + `METRICS_FAMILY`.
   - `docs/CLOSED-SANDBOX-MVP.md` §7 «Метрики sandbox (обязательные)» — same.
   - `docs/NORTH-STAR-BUILD.md` §4 could gain a `quality_per_unit_cost` row.
4. **Human confirm:** `synapse_import` was put in the `generic` family
   (reasoning in §1). If the preference is to keep the core itself strict for
   imported Synapse KPIs, flipping it to `"snn"` is a one-line change and the
   suite stays green — the domain already emits `spike_count` / `synops`.
5. **Behaviour change in §2** (spike proxies suppressed at zero cost) touches
   what `biocompute` / `synapse_import` reports print. Nothing in `eval/` or
   `docs/` cites those two numbers today, but it is a visible artifact change and
   should be a conscious merge, not a surprise.

---

## 6. Proposed STATUS Session log line

```markdown
- **2026-08-08 · Brief F — metrics envelope generalized (NL-ADR-025).** Core now
  requires only `metric_primary` + its value + `budget_ok`; spike strictness kept
  for the SNN family via plugin `METRICS_FAMILY` (D0/D1/D3/D4 = `snn`, biocompute
  / synapse_import = `generic`). Added `[economy] cost_key` →
  `quality_per_unit_cost` (demo: `examples/chip_estimate_v0`, `chip_power_mw`);
  `quality_per_kspike` / `quality_per_ksynop` unchanged. Report columns are now
  derived from what the domain returned — no `n/a` spike columns. Golden files
  freeze `report.md` + `diff` (`sandbox/tests/golden/`). Check:
  `cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"` →
  **85 passed** (was 51); all 7 examples run clean. Next: generalize
  `cli.py stress` and the UI scenario table (spike-only today).
```

---

## 7. Draft ADR — candidate NL-ADR-025

> Orchestrator: paste into `docs/DECISIONS.md` after NL-ADR-024. Not written by
> this track.

```markdown
## NL-ADR-025 — Common metrics envelope: `metric_primary` core, spikes by family

**Status:** Accepted (2026-08-08)

**Context:** `engine.run_project` demanded `spike_count`, `synops` and `f1`/`accuracy` from **every** domain, `report.enrich_economy` could only divide by spikes, and the `report.md` columns were hardcoded to spike keys. D2 `biocompute` already had to report `spike_count = 0` to get through the core, and any future non-spiking domain (cost estimate, resource budget, process node) could not exist at all. This blocked D5+ and any reuse of the core.

**Decision:**

1. **Core envelope** — every domain owes exactly three things: `metric_primary` (str, the name of its primary metric), a numeric value under that name, and `budget_ok` (bool). `spike_count` / `synops` / `f1` / `accuracy` are **optional** at the core level.
2. **Family opt-in for strictness** — a plugin may declare module-level `METRICS_FAMILY`; absent ⇒ `"generic"`. `METRICS_FAMILY = "snn"` additionally requires `spike_count`, `synops` and (`f1` or `accuracy`). D0 `snn_lif`, D1 `neuro_chip`, D3 `biosignal`, D4 `hybrid` = `snn`; D2 `biocompute` and `synapse_import` = `generic`. An unknown family value is an `EngineError` at plugin load.
3. **Strictness stays where the contract is known** — `synapse_import` keeps `_REQUIRED_SOURCE = ("accuracy", "spike_count", "synops")` on its source fixture (thin core / fat plugins, `CLOSED-SANDBOX-CODE.md` §2).
4. **Generic economy** — `[economy] cost_key` (optional `cost_unit`) in the manifest yields `quality_per_unit_cost = metric_primary / cost_key`. Existing `quality_per_kspike` / `quality_per_ksynop` keep their names and formulas (NORTH-STAR-BUILD §4). Metrics keys are never renamed. A proxy is omitted when its cost is `0` — no ratio is better than a meaningless one.
5. **Report is data-driven** — summary bullets and the `## Per scenario` columns come from what the domain actually returned; a non-spiking domain gets no `n/a` spike columns.
6. **Golden files** — `report.md` and `diff` output are frozen byte-exact in `sandbox/tests/golden/` (`wall_ms` pinned), plus a structural check against a live `anomaly_v0` run. Format drift in the customer-facing artifact now fails the suite.

**Consequences:**

- A domain with no spikes is possible without touching the core; a new domain is still an ADR (this one does not open any).
- D0–D4 + `synapse_import` behave exactly as before: 7/7 examples run clean, unit suite 51 → 85 passed.
- Any intentional report format change must regenerate the goldens: `cd sandbox && PYTHONPATH=src:tests python tests/test_report_golden.py`.
- Still spike-shaped and to be generalized separately: `cli.py` `stress` summary and the `sandbox/ui/` scenario table.
- `CLOSED-SANDBOX-CODE.md` §3 and `CLOSED-SANDBOX-MVP.md` §7 must be updated to the envelope above (they still list the old D0 required keys).
```
