# Neurolab STATUS

**Last updated:** 2026-08-05

## Summary

| Area | State |
|---|---|
| **Best lab GGUF** | hammer2 (model alone was 17/20) |
| **Demo / eval bar** | **hammer2 + contour_guard · 20/20** (ADR-047) |
| micro / diverse | 17 / 16 — not promoted |
| **Closed Sandbox** | **D0–D4** · **P01–P05** · **by_scenario split** · Gate pilot ON |
| **Pilot chat** | pack + smoke green (`PILOT-CONTOUR-CHAT.md`) |
| **Agent-eval** | **LIVE hn + agent_format · 20/20** (`:8102`) |
| **Synapse bridge** | **v0.3** · Gate ADR-054 · **pilot-contour-gate ON** (:8097) · smoke 3/3 · SOW Approved |

### Ladder

| Ver | Score |
|---|---|
| Tiny-v0 | 15 |
| hammer2 | 17 (GGUF alone) |
| micro / diverse | 17 / 16 |
| **hammer2 + guard** | **20/20** |

GGUF (use): `artifacts/outpost-tiny-hammer.Q4_K_M.gguf`  
Runtime: Commercial Outpost `[contour_guard] enabled = true`

## Next

1. Pause Tiny LoRA sheet chase  
2. (optional) richer D4 fronts / Chip PDK-adjacent later  

## Session log

### 2026-08-05 — Real by_scenario splits D1–D4

- D1 neuro_chip: activity loads `nominal` / `high_activity` / `sparse` → distinct `chip_fit_score` / power
- D2 biocompute: input bias `balanced` / `sparse` / `dense`
- D3/D4 biosignal+hybrid: signal conditions `clean` / `arrhythmia` / `noisy`
- Examples + `test_by_scenario_domains` all **split** (≥2 distinct rows); stub fallback remains for plugins without by_scenario
- Verify: `pytest tests/test_by_scenario_domains.py` (+ domain suite) green

### 2026-08-05 — Port CS-P01 Overview + CS-P02 Editor

- ★ + Port: Commercial `CS-P01`/`CS-P02` + parity; neurolab `/` + `/editor` (Run moved to `/run`)
- API: `/api/projects`, `/api/manifest`, `/api/validate` (+ save)
- Verify: UI suite P01–P05 **12 passed**; `closed-sandbox ui` → `:8765` health screens P01…P05

### 2026-08-05 — Gate enable on named pilot contour

- Commercial: `config/sovereign.pilot-contour-gate.toml` — hammer2 + guard + **`[synapse_bridge] enabled`** (:8097)
- Chat-only pilot `:8096` stays Gate-off; example.toml default still off
- Verify: `./scripts/synapse-gate-smoke.sh` → **3 pass / 0 fail** + audit `synapse.*`

### 2026-08-05 — by_scenario on all domains

- Engine `ensure_by_scenario`: stub rows for D1–D4 (+ synapse_import) from manifest names
- snn_lif stays `by_scenario_mode=split`; others `stub` (identical aggregate copy per name)
- Verify: `pytest tests/test_by_scenario_domains.py` + demo_pack

### 2026-08-04 — Port CS-P05 Ask (FR-UI-030/031)

- ★ + Port: Commercial `CS-P05-ask.html` + `parity/CS-P05.yaml`; neurolab `sandbox/ui/ask.html` · `/api/ask`
- Public risk banner mandatory; local default; CLI `contour_ask.ask`
- Verify: `pytest tests/test_ui_cs_p05.py` (+ UI suite)

### 2026-08-04 — Port CS-P04 Diff (FR-UI-020)

- ★ + Port: Commercial `CS-P04-diff.html` + `parity/CS-P04.yaml`; neurolab `sandbox/ui/diff.html` · `/api/diff`
- CLI parity: `closed-sandbox diff` shape (`n_changed` + `changed`)
- Verify: `pytest tests/test_ui_cs_p04.py` (+ CS-P03 suite) green
- Nested `by_scenario` table rows waived (API still full)

### 2026-08-04 — Per-scenario metrics (snn_lif)

- Engine: generative conditions `nominal` / `anomaly` / `noise` → `metrics.by_scenario`
- UI CS-P03 table + `report.md` § Per scenario; parity `per-scenario-metrics` → **done**
- Verify: `pytest tests/test_snn_lif.py tests/test_ui_cs_p03.py` green; rows differ by scenario

### 2026-08-03 — Demo pack (D0–D4 + UI + Gate)

- Runbook: `docs/DEMO-PACK-SANDBOX.md` · script `sandbox/scripts/demo_pack.sh`
- Verify: **6 pass / 0 fail** (~10s domains)
- Wording: Approved SOW one-liners in runbook table

### 2026-08-03 — Synapse Gate SOW wording **Approved**

- Human: OK on `docs/SYNAPSE-GATE-SOW-WORDING.md`
- Handoff §10 / checklist human OK ticked
- Agents may reuse §3–§5; Gate flag still default **off** until pilot enable

### 2026-08-03 — Synapse Gate SOW wording draft (await human)

- (superseded by Approved above)

### 2026-08-03 — D4 `hybrid` opened (NL-ADR-024)

- Composition: `[front]` synthetic ECG/EEG → encode → `[backend]` `snn_lif`
- Example `hybrid_ecg_snn_v0` · metrics `hybrid_pipeline`
- Domain suite D0–D4 now runnable
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/hybrid_ecg_snn_v0/project.toml`

### 2026-08-03 — D2 closed · D3 `biosignal` opened (NL-ADR-023)

- D2 v0.1 marked complete (`boolean_grn_v0`)
- D3: `synthetic_ecg_v0` / `synthetic_eeg_v0` · threshold encode · LIF classify
- Example `biosignal_ecg_v0` · not clinical
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/biosignal_ecg_v0/project.toml`

### 2026-08-03 — D2 `biocompute` opened (NL-ADR-022)

- Domain `boolean_grn_v0` · example `biocompute_grn_v0`
- Metrics: accuracy/f1 + `bio_*` · wet-lab explicitly out
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/biocompute_grn_v0/project.toml`

### 2026-08-03 — FPGA named target `fpga_snn_lite_v0` (NL-ADR-021)

- Target + LUT/BRAM/DSP proxies · example `chip_fpga_lite_v0`
- CLI writes `out/chip_export.json` when `chip_export` present
- Still no bitstream / vendor SDK · tests extended
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/chip_fpga_lite_v0/project.toml`

### 2026-08-02 — D1 `neuro_chip` opened (NL-ADR-020)

- Domain plugin + example `chip_estimate_v0` · target `generic_neuromorphic_v0`
- Metrics: `chip_area_mm2`, `chip_power_mw`, `chip_fit_score` + disclaimer
- Tests: `tests/test_neuro_chip.py` · run: `closed-sandbox run examples/chip_estimate_v0/project.toml`
- Non-goals locked: no fab/PDK/GDSII / measured silicon claims

### 2026-08-02 — Commercial Gate implemented (ADR-054)

- Outpost: `[synapse_bridge]` · `POST /v1/synapse/escalate` · audit `synapse.*`
- Live smoke **3/3** on hammer2 (`sovereign.synapse-gate.toml` `:8097`)
- Handoff checklist + `SYNAPSE-BRIDGE.md` → **implemented**
- Next agreed: **D1 neuro_chip**

### 2026-08-02 — Commercial Gate handoff (#1)

- Doc: `docs/COMMERCIAL-GATE-HANDOFF.md` — shape A; (superseded by ADR-054 ship above)

### 2026-08-02 — Investor one-pager + build ladder + economy v0

- Docs: `INVESTOR-NORTH-STAR.md` · `NORTH-STAR-BUILD.md` · INDEX / STRATEGY / GRANTS pointers
- Code: sandbox `quality_per_kspike` / `quality_per_ksynop` in report JSON+MD; stress summary mean
- Verify: `cd sandbox && PYTHONPATH=src python -m pytest tests/test_cli_report.py -q`
- Next lever: Commercial Gate handoff checklist **or** next Sandbox ★/Port screen

### 2026-08-02 — North star documented (NL-ADR-019)

- Thesis: cover frontier strengths with **our system** + measured resource economy; distinct breed (not Kimi/Grok clone)
- Docs: `STRATEGY.md` (north star + delivery A/B/C) · `DECISIONS.md` NL-ADR-019 · pointers in GOALS / SCALE-PLAN / SYNAPSE-BRIDGE / INTELLECTUAL-CANON / AGENTS / INDEX
- No code; no Mid/Large kickoff — narrative lock only

### 2026-08-02 — Port CS-P03 (NL-ADR-018)

- Host **A**: neurolab `sandbox/ui/` + `ui_server.py` · `closed-sandbox ui` → `:8765`
- FR-UI-010/011/012 wired to `run_project` + metrics/report export
- Tests: `tests/test_ui_cs_p03.py` (3) · unit suite green (synapse fixture assert refreshed)
- Parity: Commercial `parity/CS-P03.yaml` → ported (cancel + per-scenario waived)
- Verify: `cd sandbox && PYTHONPATH=src python -m closed_sandbox.cli ui`

### 2026-08-02 — ★ CS-P03 promoted (move pipeline forward)

- Human: Lab soft-OK; tweaks later in ops; **двигать дальше** → ★ promote
- Commercial: `CS-P03-run-results.html` · `parity/CS-P03.yaml` · hub + Studio manifest Prod ★
- Neurolab: `docs/STUDIO-STAR-REVIEW-CS-P03.md` closed ★
- **No Port yet** — production UI waits explicit Port kickoff

### 2026-08-02 — Studio review: soft-OK, ★ deferred

- Human: Lab mocks look fine for now; future tweaks possible
- (superseded same day by ★ promote above)

### 2026-08-02 — Studio ★ review opened (CS-P03)

- Design Studio up · Closed Sandbox hub + CS-L01…05 browsable
- First Port slice candidate: **CS-L03 Run+Results** (FR-UI-010/011/012)
- Checklist: `docs/STUDIO-STAR-REVIEW-CS-P03.md` — waiting human ★ / правки
- No Port / no CS-P* until human says `★ CS-P03`

### 2026-08-01 — Synapse v0.3 → sandbox → ask ✅

- Fixture from `2026-08-01-e5-brains-v2-skip-llm.json` · class_fix=**specialist** **0.8636**
- Exporter handles brains-v2 rows; `contour_ask` uses dynamic class_fix
- Ask 3/3 PASS on `:8098` · report `sandbox/reports/e5-roles-ask-20260801.md`
- Bridge pointer already v0.3; STATUS Synapse row updated

### 2026-08-01 — Design Studio Closed Sandbox confirmed

- Commercial section already live (hub + CS-L01…05); pipeline §5–8 + FR matrix marked Lab done
- Rule `08-design-mockups` lists `design/sandbox/`; parity folder ready for ★ yaml
- Open: `cd ~/Projects/AI-Platform-Vision && ./scripts/design-studio.sh` → **Closed Sandbox**
- Next: human review → promote CS-P03 ★ (no UI code before)

### 2026-08-01 — Agent format LIVE 20/20

- Rebuilt `sovereignd` into Commercial `target/` (not sandbox cache)
- Live `:8102` hn + `[agent_format]` → agent-v0 **20/20**
- Raw `eval/results/raw/agent-v0-live-format-20260801/` · report `agent-v0-runtime-format.md`
- Pilot contour sheet untouched

### 2026-07-31 — Agent format v2 (+ plan_steps) → 20/20

- Added `agent_plan_steps_airgap` (GGUF→toml→sovereignd→/health, no Docker)
- Lab mirror: hn + format **20/20** · `eval/results/agent-v0-runtime-format.md`
- Commercial module updated; live still needs release rebuild

### 2026-07-31 — Agent format runtime (+2)

- Commercial: `agent_format.rs` + `[agent_format]` + chat hook; unit **5 passed**
- Lab mirror: `scripts/agent_format_runtime.py` (binary was stale pre-hook)
- Score: hammer2+format **18/20** · **hn+format 19/20** (plan+budget closed)
- Config: `config/sovereign.agent-format.toml` · result `eval/results/agent-v0-runtime-format.md`
- Next: `cargo build -p sovereign-daemon --release` in Commercial to confirm live

### 2026-07-31 — Agent mixed pack (30d) — plateau

- Mix 49 (15 plan / 15 budget / **12 self_check**) · continue hn → `20260730-mps-agent-mix`
- agent-v0 **17/20** flat vs hn: `self_check` retained; plan/budget still 1
- Verdict: Tiny SFT saturated on those two formats; prefer runtime next
- Result: `eval/results/agent-v0-agent-mix.md`

### 2026-07-30 — Agent plan+budget focus (30c) — miss

- Data focus 46 (20 plan + 20 budget, thin retain) · continue hn → `20260730-mps-agent-pb`
- agent-v0 **16/20** (−1): plan/budget still 1; `self_check` regress 2→1
- Keep **hn 17/20** as best agent exp; do not promote pb
- Result: `eval/results/agent-v0-agent-pb.md`

### 2026-07-30 — Agent hard-neg LoRA (+1)

- Data: `tiny-lora-agent` **24→47** (hard-neg on plan/self_check/budget)
- Train: `20260730-mps-agent-hn` · hammer2 init · f32 · 12/12 · loss 2.467
- agent-v0: **17/20** (+1) — `self_check` 1→2; `plan_tool_mix` + `budget` still 1
- GGUF: `outpost-tiny-agent-hn.Q4_K_M.gguf` · result `eval/results/agent-v0-agent-hn.md`
- Pilot untouched; not promoted

### 2026-07-30 — Roles v0.2 sandbox re-run ✅

- Synapse BRAIN-BRIDGE v0.2 · class_fix=`stage_vote` · brain=`explain_plan`.  
- Fixture acc **0.8598**; ask 3/3 PASS after CANONICAL FACTS prompt.  
- Report: `sandbox/reports/e5-roles-ask-2026-07-30.md`.

### 2026-07-30 — Agent-eval LoRA (track B)

- Train: hammer2 init → `tiny-lora-agent` · f32 · lr 1e-5 · 1 ep · MPS · **6/6 no NaN** (`20260729-mps-agent-f32`)
- Export: `artifacts/outpost-tiny-agent.Q4_K_M.gguf` · config `sovereign.agent-lora.toml` :8097
- agent-v0 re-score: **16/20** (flat vs hammer2 baseline) — format gaps unchanged
- Result: `eval/results/agent-v0-agent-lora.md`; pilot hammer2+guard **untouched**
- Next lever if retry: denser fail-ID data or +1 epoch — not Mid

### 2026-07-29 — E5 brains v2 (+0.37 pp)

- Diagnostic: only 4/9 escalate-wrong recoverable via other-stage argmax
- `stage_vote` + outpost payload v2 → acc **0.8598** (+0.37 pp vs stub); oracle still 0.8902
- Tiny v2 ≈ stage_vote; Mid size still wrong lever for class fix
- Report: `sandbox/reports/e5-brains-v2-2026-07-29.md`

### 2026-07-29 — Mid 14B escalate brain (NL-ADR-016)

- Found LM Studio Qwen2.5-**14B** Q4 (~8.4G); config `sovereign.mid-escalate.toml` `:8099`
- Bench: Mid parse 18/18 · **Δacc=0** vs stub (same as Tiny) · wall ~99s
- Verdict: size ≠ lever for top-k logits re-pick; oracle gap remains +3.4 pp
- Report: `sandbox/reports/e5-mid14-escalate-2026-07-29.md`

### 2026-07-29 — Escalate → Outpost chat (lab probe)

- Synapse `brain=outpost` + `bench_outpost.py`; hammer2 :8098
- Acc stub=outpost **0.8561**; oracle 0.8902; **18/18 parse OK**, Δacc=0
- Report: `sandbox/reports/e5-outpost-brain-2026-07-29.md`
- Wiring proof done; accuracy lift deferred (payload/Mid)

### 2026-07-29 — Step B: live E5 export → sandbox

- Synapse bench PASS → `2026-07-29-e5-brain-escalate.json` (acc 0.8561, esc 0.0682, oracle 0.8902)
- Exporter `sandbox/scripts/export_synapse_e5_fixture.py`; fixture refreshed; diff vs CARD tiny
- Report: `sandbox/reports/e5-live-export-2026-07-29.md`
- Cycle: bench → export → `closed-sandbox run` is reproducible

### 2026-07-29 — Step A: ask on E5 import metrics

- Import run + Outpost `:8098` ask ×3 → `sandbox/reports/e5-ask-2026-07-29.md`
- Verdict: oracle/host-wrap OK; Tiny still confuses escalate≠SNN on Q1
- Prompt: `contour_ask` synapse_import-aware; example `base_url` → `:8098`
- Next: step B (live Synapse export) or agent data on escalate semantics

### 2026-07-29 — Sandbox speed + synapse_import

- numpy LIF + lean train + early-stop → wall **~7.5s → ~0.26s**/seed; f1 **0.93±0.04**
- Domain `synapse_import` + example `synapse_e5_import` (frozen E5 CARD KPIs, no torch)
- Tests **14 passed**; note `sandbox/reports/anomaly-v0-speed-synapse-import-2026-07-29.md`
- Stack path now: Synapse fixture → sandbox → optional `ask` (hammer2)

### 2026-07-29 — Sandbox stress + train harden

- Finding: seed variance was bad (f1 mean 0.82 ± 0.12, min 0.43)
- Fix: more train (120), 20 epochs + shuffle + lr decay; `wall_ms`; CLI `stress`
- After: f1 **0.90 ± 0.06**, min **0.76**, budget_ok 1.0 (20 seeds)
- Report: `sandbox/reports/anomaly-v0-stress-2026-07-29.md`
- Tests: unit **12 passed**; Synapse+Neurolab «через sandbox» = ask today, not one binary
- Synapse e5 smoke blocked here (no torch in env) — separate lab

### 2026-07-29 — Parallel briefs A–D complete

| Track | Result | Headline |
|---|---|---|
| **A** Studio | `docs/AGENT-BRIEFS/results/A.md` | Commercial `design/sandbox/` CS-L01…05 + hub |
| **B** Pilot | `docs/AGENT-BRIEFS/results/B.md` | pilot pack + smoke 5/5 |
| **C** Agent | `docs/AGENT-BRIEFS/results/C.md` | agent-v0 · hammer2 **16/20** · data pack |
| **D** Bridge | `docs/AGENT-BRIEFS/results/D.md` | synapse `BRAIN-BRIDGE.md` + neurolab pointer |

### 2026-07-29 — Brief C: agent-eval baseline

- Rubric + 10 prompts: `eval/agent-rubric.md`, `eval/prompts/agent-v0.jsonl`
- hammer2 model-only (guard off :8097): **16/20** → `eval/results/agent-v0-hammer2-baseline.md`
- Data lever draft: `datasets/tiny-lora-agent/` (24 msgs); result `docs/AGENT-BRIEFS/results/C.md`
- Next (human): optional short LoRA on agent pack → re-score agent-v0; no Mid; pilot sheet untouched

### 2026-07-29 — Brief B: pilot contour chat pack

- Pack: `docs/PILOT-CONTOUR-CHAT.md` (hammer2 + guard 20/20, demo script, smoke)
- Smoke ran on Mac: `eval/results/pilot-contour-smoke.md` — all 5 checks green
- CARD / INDEX / AGENTS hygiene; result → `docs/AGENT-BRIEFS/results/B.md`
- Next (human): Commercial pack / customer wording

### 2026-07-29 — Agent briefs A–D launched

- Wrote `docs/AGENT-BRIEFS/` (README + A Studio · B pilot · C agent-eval · D Synapse bridge)
- Launching 4 parallel agents; results → `docs/AGENT-BRIEFS/results/`
- Next: merge results into Done when each `results/*.md` lands

### 2026-07-28 — UI pipeline + FR (Design Studio first)

- Spec: `docs/CLOSED-SANDBOX-UI-PIPELINE.md` — раздел Closed Sandbox, Prod★ vs Lab, конвейер как Outpost DESIGN-TO-PROD
- FR: `docs/CLOSED-SANDBOX-UI-REQS.md` — FR-UI-001…031 + матрица трассировки
- ADR-015; wired UI.md / AGENTS / INDEX / MVP / CLOSED-SANDBOX-AGENTS
- **Next (Commercial):** `design/sandbox/` + category in Studio manifest + hub; no UI code yet

### 2026-07-28 — human confirm full suite 11+3

- Host Mac: unit 11 passed, integration 3 passed (`test_ask_cli` + API ask ×2)
- Sheet: `docs/CLOSED-SANDBOX-VERIFY.md` updated

### 2026-07-28 — verify + expand sandbox tests

- Sheet: `docs/CLOSED-SANDBOX-VERIFY.md`
- Unit: CLI/report + contour_ask error paths → **11 passed** (`not integration`)
- Integration: conftest boots Outpost; API ask ×2 + **CLI ask** → **3 passed**
- Human confirm earlier: integration 2/2 on Mac; suite now 3
- MVP §9 DoD mostly checked; public live ask still optional

### 2026-07-28 — ask ↔ Outpost integration tests

- `sandbox/tests/test_ask_outpost.py` (+ `outpost_util.py`): boots `sovereignd` + hammer2 on :8098
- Config: `config/sovereign.sandbox-ask.toml`
- Smoke script: `sandbox/scripts/run_ask_outpost_smoke.sh`
- `pytest -m integration` → **2 passed** (f1/budget + spike YES/NO)
- Note: needs Metal/GPU host access (not Cursor sandbox); GGUF + Commercial release binary
- Fast suite: `pytest -m "not integration"` (5 unit tests)

### 2026-07-28 — Closed Sandbox v0.1 code (D0 snn_lif)

- Package `sandbox/`: manifest, engine, domains/snn_lif, report, contour_ask, CLI
- Example `examples/anomaly_v0`: run → F1≈0.82, budget_ok, metrics.json + report.md
- Tests: 5 passed (`PYTHONPATH=src pytest`)
- How: `cd sandbox && PYTHONPATH=src python -m closed_sandbox.cli run examples/anomaly_v0/project.toml`
- Next: Outpost ask smoke; UI still out of v0.1 core

### 2026-07-28 — UI canon (scientific / industrial)

- Added `docs/CLOSED-SANDBOX-UI.md` · ADR-014
- Exemplars: ParaView, Napari, Grafana, MLflow, KiCad, VS Code; HMI/ISA-101
- Books: Munzner, Tufte, High Performance HMI, Norman, Cooper, Few
- Order: CLI first → thin local web UI; no consumer AI aesthetics
- Wired into AGENTS map / INDEX / MVP / STATUS

### 2026-07-28 — Sandbox agent canons (science / code / industry)

- Entry: `docs/CLOSED-SANDBOX-AGENTS.md`
- New: `CLOSED-SANDBOX-CODE.md`, `CLOSED-SANDBOX-INDUSTRY.md`; science canon clarified
- ADR-013; wired INDEX / AGENTS / MVP / sandbox README
- Formula for agents: MVP × science × industry × code → measurable sandbox/

### 2026-07-26 — Multi-domain sandbox (silicon + biotech)

- Vision: one platform, domain plugins D0–D4; biotech = digital biocompute/biosignal, not wet-lab
- ADR-012; MVP §2 domains; canon §3b bio adjacency; `domain` in manifest; `domains/` package layout
- v0 still only snn_lif anomaly — biotech packs after D0 demo

### 2026-07-26 — Grant programs map

- Fixed: `docs/CLOSED-SANDBOX-GRANTS.md` (S0→S3 ladder; Innosuisse/national/Eurostars; Chips JU; EIC Open)
- Linked from MVP, INDEX, AGENTS, sandbox README
- Order: demo → legal entity → national/Innosuisse → consortium/Chips → EIC Open

### 2026-07-26 — Closed Sandbox: public LLM opt-in

- `ask`: default `provider=local` (Outpost/hammer2); early lab may use `provider=public` + env key
- Aligned with CONTOUR-EGRESS / ADR-009; ADR-010 updated; never silent cloud egress
- Next: implement `sandbox/` with both providers

### 2026-07-26 — Closed Sandbox MVP + research canon

- MVP: `docs/CLOSED-SANDBOX-MVP.md` · ADR-010 · `sandbox/README.md`
- Canon under frame: `docs/CLOSED-SANDBOX-CANON.md` · ADR-011 (LIF first; bio fidelity deferred; adopt/defer)
- Anchors: Gerstner; EdgeSNN survey; Innatera/BrainChip/NIR as landscape — not fab copy
- Next: implement `sandbox/` package (2-week plan in MVP doc)

### 2026-07-21 — 20/20 with formal guard

- Fresh `cargo build --release -p sovereign-daemon`
- Extended guard: `ru_formal` canned 2 sentences
- Eval → **20/20** · `eval/results/tiny-hammer2-plus-guard.md`

### 2026-07-21 — contour runtime guard

- clarify + refuse closed; first full eval 19/20 (formal=1)
- Formal added to guard → 20/20

### 2026-07-21 — micro / diverse

- micro 17, diverse 16 — not promoted
