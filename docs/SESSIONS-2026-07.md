# Session log archive — 2026-07

> **Что это:** записи журнала сессий **старше 2026-08-01**, вынесенные из
> [`../STATUS.md`](../STATUS.md) 2026-08-08 без изменения текста.
> Порядок — как в STATUS: сверху новее.
>
> Живой статус и текущий фокус — только в [`../STATUS.md`](../STATUS.md).
> Здесь ничего не редактируем: это история.

---

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
