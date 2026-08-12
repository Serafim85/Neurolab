# DECISIONS — Neurolab ADR log

> Формат: **Status** · **Context** · **Decision** · **Consequences**  
> Не удалять — помечать Superseded.

---

## NL-ADR-001 — Lab scope: weights only, Outpost executes

**Status:** Accepted (2026-07-18)

**Context:** Need a place for model R&D without destabilizing commercial runtime.

**Decision:** Neurolab owns cards, data manifests, train/export, eval. Inference product remains `AI-Platform-Vision`.

**Consequences:** No training pipelines in Commercial; smoke via sovereignd binary + Lab config only.

---

## NL-ADR-002 — Dense Qwen2.5-3B as Tiny v0 base

**Status:** Accepted (2026-07-18). **Superseded** by NL-ADR-028 (2026-08-13).

**Context:** Need locked baseline; Outpost already has pull preset `qwen2.5-3b-instruct-q4`.

**Decision:** Lock **Qwen2.5-3B-Instruct Q4_K_M** as Outpost-Tiny backbone. Not 1.5B for v0; not MoE.

**Consequences:** Baseline scored 14/16; LoRA targets this base. Change of base = new ADR + human.

---

## NL-ADR-003 — Micro-MoE = product suite, not arch MoE

**Status:** Accepted (2026-07-18)

**Context:** Desire for several mini networks vs monolith.

**Decision:** Experts are separate dense GGUFs + router; arch-level MoE deferred to Large scale-out.

**Consequences:** See `MICRO-MOE.md`; one new expert per iteration.

---

## NL-ADR-004 — Engineering doctrine: reliability, quality, min→max

**Status:** Accepted (2026-07-18)

**Context:** Founder requires full agent docs, measurable quality, lean resource use.

**Decision:** All model work follows `ENGINEERING.md` cycle (baseline → one lever → eval → CARD/STATUS). Mottos: reliability & quality; minimize compute/time for maximum measured gain.

**Consequences:** Agents reject vibe-only claims; Session log mandatory.

---

## NL-ADR-005 — Documentation set for agents

**Status:** Accepted (2026-07-18)

**Context:** Lab needed the same operational rigor as Commercial AGENTS.md.

**Decision:** Canonical set: `AGENTS.md`, `ARCHITECTURE`, `GOALS`, `INTEGRATION`, `SCALE-PLAN`, `ENGINEERING`, `DECISIONS`, `STATUS`.

**Consequences:** Agents start at `AGENTS.md`; architecture changes update `ARCHITECTURE.md` + ADR.

---

## NL-ADR-006 — Model Construct: flexible slots + hardware profiles

**Status:** Accepted (2026-07-18)

**Context:** Future direction of “our neural net” is unknown (Tiny only vs suite vs Mid/Large). Need foundations for flexibility, configurability, scale, and light auto-fit to hardware — without freezing a single monolith or building magic NAS.

**Decision:**

1. Evolve models as a **Model Construct**: declarative catalog of **slots** (micro-nets), **router**, **hardware profiles**, **autotune policy** — see `docs/CONSTRUCT.md`, `construct/example.toml` (schema v0.1).
2. **Add/remove/configure** micro-nets = edit catalog + weights + CARD; API surface of Outpost stays stable.
3. **Autotune v1** = select richest profile whose peak RAM fits `memory_limit_mb × safety_factor`; lock profile after boot; audit selection. No online retrain.
4. Implementation order: Lab contract now (S0–S2) → Outpost Gate B+ load/autotune (S3–S5). Tiny LoRA is **not** blocked on full runtime construct.
5. Align naming/fields with Commercial `agents.toml` / ModelPool where possible; construct is the **superset pack format**.

**Consequences:**

- Agents design new capabilities as **slots + skills**, not one-off forks.
- Changing locked Tiny *base* still needs ADR; adding an `extract` slot does not.
- Over-automation (continuous model swap mid-flight, auto LoRA) is out of scope until explicit ADR.

---

## NL-ADR-007 — Intellectual Canon for the model lineage

**Status:** Accepted (2026-07-18)

**Context:** Development needs a shared intellectual base (books, papers, lab engineering notes) aimed at the future, not ad-hoc blog following. Outpost lineage must stay powerful and forward-compatible while remaining lean (offline, Construct, min→max).

**Decision:**

1. Maintain living canon: `docs/INTELLECTUAL-CANON.md`.
2. **Pillars:** dense Transformer first; scaling laws (Kaplan/Chinchilla); post-training as primary lever; product Construct before arch-MoE; cautious test-time compute; interpretability/audit for contour; GGUF local stack; systems reliability.
3. Agents cite canon (paper/book + adopt/defer) in Session log or ADR when changing architecture, train recipe, or scale step.
4. Curate Anthropic (interpretability, inverse scaling) and OpenAI (training systems) as **engineering literacy**, not as blueprints to clone frontier clusters.
5. Refresh canon quarterly or on base/Mid transitions; new entries need one-line “take / don’t take for Outpost”.

**Consequences:**

- Reading lists are filtered by Contour + Measure + Construct.
- Arch-MoE and cluster networking stay deferred until L6/dc evidence.

---

## NL-ADR-008 — Construct Advisor (intent × hardware → propose)

**Status:** Accepted as **planned** (2026-07-18) — design only; not Phase-1 blocking

**Context:** Founder proposes a small evaluator agent that reads user intent and system params, then recommends the model variant the hardware can run and the task needs — custom setup for concrete jobs.

**Decision:**

1. Adopt as **Construct Advisor** in `docs/CONSTRUCT.md` §7b (implementation step S6).
2. Output is always **propose + human Accept** (or rules-only A1), never silent mid-session model swap.
3. v0 path: **rules + skill tags + RAM filter**; LM advisor optional later (A2).
4. Does not block Tiny LoRA or Construct S0–S4.
5. Advisor selects only from installed catalog (or explicitly suggests pull) — no invented 70B.

**Consequences:**

- Product story: “мастер настройки под задачу и железо”.
- Agents may extend intent→slot tables in Lab; runtime wiring waits until catalog+profiles exist.

---

## NL-ADR-009 — Contour-safe egress: client cloud yes, public LLM default off

**Status:** Accepted (2026-07-18) — policy; runtime connectors later

**Context:** Refuse-cloud LoRA must not reject the customer’s own cloud. Product should connect into the client contour/private cloud when asked; public cloud LLM networks may exist as optional connectors but must stay disabled by default (offline-first).

**Decision:**

1. Policy doc: `docs/CONTOUR-EGRESS.md` — zones Local / Client cloud / Public LLM.
2. **Model (Tiny LoRA):** contour-safe — refuse unapproved public LLM exfil; allow/neutral on customer private cloud.
3. **Runtime:** client-cloud connectors = allowlist, opt-in; `egress.public_llm.enabled = false` by default; no phone-home (Commercial B8).
4. Does not weaken localhost bind defaults; any default-on public egress requires ADR + human.

**Consequences:**

- LoRA data uses contour-safe prompts, not blanket anti-cloud.
- Commercial implementation of connectors is backlog after pilot need; Lab owns behavior + policy text now.

---

## NL-ADR-010 — Closed Sandbox track (SNN studio, not fab)

**Status:** Accepted (2026-07-26)

**Context:** Exploring a product: closed-contour tool to design/test compact brain-inspired networks (and later map toward neuromorphic targets). Must not derail Outpost-Tiny supply chain or pretend to be full chip EDA.

**Decision:**

1. Lab hosts prototype under `sandbox/` + canon `docs/CLOSED-SANDBOX-MVP.md`.
2. **v0 object:** SNN / brain-inspired network + sandbox metrics (accuracy, spike/energy proxy) + report; one vertical (edge anomaly).
3. **AI `ask`:** target = Outpost-Tiny (**hammer2**) in contour; **public cloud LLM allowed as explicit opt-in** for early lab/dev (same spirit as NL-ADR-009: default off, never silent).
4. **Out of v0:** ASIC/PDK/tape-out, industrial machine physics, multi-architecture zoo.
5. Productized UI/runtime may move to Commercial later; weights/eval for the assistant stay in Lab.
6. Tiny LoRA / Construct remain the default Lab focus unless STATUS says otherwise for a session.

**Consequences:**

- Coding can start in `sandbox/` without opening Mid/Large/arch-MoE.
- Grants/jurisdiction (e.g. Luxembourg) are non-blocking; demo first.
- Expanding to fab-style EDA or factory digital twins requires a new ADR.
- Sandbox must implement `provider = local | public`; keys via env; pilot defaults stay local.
- Grant targeting lives in `docs/CLOSED-SANDBOX-GRANTS.md` (demo first; EIC Open after pilots; Chips JU via consortium).

---

## NL-ADR-011 — Sandbox canon + LIF first (biology → engineering)

**Status:** Accepted (2026-07-26)

**Context:** Product frame alone is not enough: team needs shared adopt/defer from neuroscience, SNN literature, and comparable startups — without turning v0 into biophysical simulation or organoid research.

**Decision:**

1. Living canon: `docs/CLOSED-SANDBOX-CANON.md` (separate from Outpost `INTELLECTUAL-CANON.md`).
2. **v0 neuron model:** `snn_lif` only; biological fidelity (HH, STDP-as-product, dendrites, wetware) **deferred**.
3. Adopt for v0: spikes/events, sparsity → energy proxy (`spike_count` / synops), edge task, measure-first.
4. New `network.kind` or marketing claim of “faithful brain model” requires ADR + canon update.
5. Canon cites surveys/startups as *orientation*; sandbox metrics remain the acceptance test.

**Consequences:**

- Reading list and competitor map live in canon; MVP stays the build contract.
- Agents must cite adopt/defer from CLOSED-SANDBOX-CANON when changing sandbox architecture.

---

## NL-ADR-012 — Multi-domain sandbox (silicon + biotech), wet-lab out

**Status:** Accepted (2026-07-26)

**Context:** Want one closed-contour sandbox that can later serve neuromorphic *and* biotech compute themes (bacterial/GRN abstractions, biosignals), without building an in-house wet lab or exploding v0 scope.

**Decision:**

1. Product = **platform core** (manifest → run → metrics → report → ask) + **domain plugins**.
2. **v0 implements only D0** `snn_lif` (anomaly). Layout `domains/` prepared for D1–D4.
3. Later domains: `neuro_chip`, `biocompute` (digital only), `biosignal`, `hybrid`.
4. **Out forever for Lab v0–v1:** growing organoids/bacteria, PDK/tape-out as core business.
5. Biotech R&D LLM assistant (Mid+) remains a separate model track; sandbox domains do not require it for D0.

**Consequences:**

- Coding must not hardcode “SNN-only forever”; dispatch by `project.domain`.
- New domain = ADR note + canon row + plugin package.
- Grants narrative may mention dual-industry platform; demos stay D0 until metrics exist.

---

## NL-ADR-013 — Sandbox agent doc set (science / code / industry)

**Status:** Accepted (2026-07-28)

**Context:** Agents need maintainable, readable, scalable code grounded in serious science *and* industry — without one mega-doc or mixing Outpost LLM canon with SNN studio.

**Decision:**

1. Entry map: `docs/CLOSED-SANDBOX-AGENTS.md`.
2. Four canons beside MVP: **science**, **code**, **industry**, **UI** (`CLOSED-SANDBOX-UI.md`), plus **grants** map.  
   (UI added formally in NL-ADR-014.)
3. Code canon inherits Lab `ENGINEERING.md`; adds domain-plugin contract and sandbox DoD.
4. Industry canon owns buyers/standards/competitors; science canon owns papers/adopt-defer; no wet-lab/fab as Lab product.
5. Agents must follow CLOSED-SANDBOX-AGENTS ritual when working under `sandbox/`.

**Consequences:**

- New sandbox architecture → update CODE + maybe CANON/INDUSTRY, not only chat.
- Outpost Tiny docs stay in INTELLECTUAL-CANON / TRAIN-TINY-LORA.

---

## NL-ADR-014 — UI canon for Closed Sandbox (scientific / industrial)

**Status:** Accepted (2026-07-28)

**Context:** Product will have a UI after CLI; agents need a canon so interfaces follow scientific/industrial HMI practice — not consumer AI SaaS aesthetics — with books and exemplar tools.

**Decision:**

1. Living canon: `docs/CLOSED-SANDBOX-UI.md`.
2. Ship order: CLI+report → thin local web UI → multi-domain workspace; CLI remains first-class.
3. Pillars: workflow-first, progressive disclosure, situation awareness, alarm-color discipline, contour honesty (visible public LLM).
4. Exemplars: ParaView, Napari, Grafana, MLflow/W&B compare, KiCad, VS Code; High Performance HMI / ISA-101; vendor neuromorphic tooling for metrics clarity — not ChatGPT/Notion clones.
5. Tier-A books: Munzner, Tufte, High Performance HMI Handbook, ISA-101; then Norman, Cooper, Few.
6. UI widgets are domain-pluggable like CODE plugins.

**Consequences:**

- UI work must cite CLOSED-SANDBOX-UI in session ritual.
- ADR-013 agent set extended by UI canon (see CLOSED-SANDBOX-AGENTS).
- No UI-only work that skips engine metrics DoD.

---

## NL-ADR-015 — Closed Sandbox UI via Design Studio (FR → Lab → ★ → Port)

**Status:** Accepted (2026-07-28)

**Context:** UI needed after CLI v0.1, but coding screens without a professional design→prod conveyor would recreate the Outpost mock/prod drift problem. Commercial already has Design Studio + `DESIGN-TO-PROD.md`. Sandbox must inherit that discipline and keep FR↔mock traceability.

**Decision:**

1. Specs live in neurolab: `CLOSED-SANDBOX-UI-PIPELINE.md` + `CLOSED-SANDBOX-UI-REQS.md` (FR-UI-* ids).
2. Mockups live in Commercial Design Studio under a dedicated category **`closed-sandbox`**, with explicit **Prod mockups ★** vs **Lab / Dev mockups** (Lab never Ports).
3. Each mock requires `fr_ids[]` + CLI parity command; promote Lab → Prod only by human; Port only after ★ + parity yaml (same gate idea as Outpost ≥90%).
4. No production UI code until design-phase DoD (pipeline §8); host of shipped UI (neurolab vs Commercial `/ui/`) deferred to Port ADR.
5. Agents must not invent a parallel Figma/React process outside Studio.

**Consequences:**

- Next UI work = Studio section + Lab placeholders in Commercial, not React in neurolab.
- STATUS Next: Design Studio Closed Sandbox section before UI v0.2 code.

---

## NL-ADR-016 — Mid as escalate brain (lab), not Tiny pilot swap

**Status:** Accepted (2026-07-29)

**Context:** E5 live Outpost brain with hammer2 (3B) parsed 18/18 escalate rows but Δacc vs stub = **0**. Oracle gap +3.4 pp. Tiny ceiling on top-k logits; SCALE-PLAN L5 Mid available on disk (LM Studio Qwen2.5-14B Q4).

**Decision:**

1. Keep **hammer2 + guard** as pilot contour chat (20/20) — unchanged.  
2. Trial **Qwen2.5-14B-Instruct-1M Q4_K_M** only as **E5 escalate brain** (`config/sovereign.mid-escalate.toml` · `:8099`).  
3. Path is external LM Studio cache — **not** committed; not promoted to default Construct `chat` without new ADR + eval.  
4. Success = measurable acc lift vs stub/tiny on `bench_outpost.py`; failure = document and keep Tiny escalate or mock.

**Consequences:**

- M1 16GB is tight (~8.4 GB weights); small `context_size`, no concurrent Tiny+Mid.  
- Commercial Gate still separate; this is lab wiring/KPI only.

---

## NL-ADR-017 — Agent format residue → runtime (not more Tiny SFT)

**Status:** Accepted (2026-07-31)

**Context:** agent-v0 LoRA ladder (30a→30d) plateaus at **17/20**. Sticky fails: `plan_tool_mix`, `budget_sentences`. Focus/mixed packs did not close them; focus regresses `self_check`.

**Decision:**

1. Stop Tiny agent SFT chase for those two formats.  
2. Close them in **Commercial Outpost** via `[agent_format]` (canned + normalize), sibling to ADR-047 contour_guard.  
3. Lab bar: **hn + agent_format = 20/20** on agent-v0 (includes air-gap `plan_steps`). Pilot contour sheet unchanged.  
4. Lab mirror: `scripts/agent_format_runtime.py` until release `sovereignd` rebuild wires the chat hook live.

**Consequences:**

- Code lives in Commercial `sovereign-core/src/agent_format.rs` (default off).  
- Enable with neurolab `config/sovereign.agent-format.toml`.  
- Optional later: `plan_steps` air-gap rule (separate).

---

## NL-ADR-018 — Closed Sandbox UI host = neurolab `sandbox/ui/` (CS-P03 Port)

**Status:** Accepted (2026-08-02)

**Context:** CS-P03 ★ approved. PIPELINE §6 offered A (neurolab local web) / B (Commercial `/ui/`) / C (Outpost embed). First Port slice is Run+Results with CLI parity to `closed-sandbox run`; mixing into Outpost Prod would blur products.

**Decision:**

1. **Variant A:** ship production UI under **neurolab** `sandbox/ui/` + `closed_sandbox.ui_server` (stdlib HTTP).  
2. CLI entry: `closed-sandbox ui` → `http://127.0.0.1:8765/` (CS-P03).  
3. Commercial Design Studio keeps ★ mocks + `parity/CS-P03.yaml`; no Port into `crates/sovereign-api/static/` for this vertical.  
4. B/C remain open for a later ADR if product wants Sandbox inside Outpost.

**Consequences:**

- Engine stays SoT; UI only dispatches `run_project` + report writers.  
- Cancel mid-run waived until engine supports cooperative cancel.  
- Per-scenario: `snn_lif` emits `metrics.by_scenario` (generative conditions); UI/report consume it (parity item closed 2026-08-04). Other domains may still fall back to aggregate row copy until they emit `by_scenario`.
- **CS-P04 Diff** Ported 2026-08-04 on same host (`/diff`, FR-UI-020); nested `by_scenario` table display waived.
- **CS-P05 Ask** Ported 2026-08-04 (`/ask`, FR-UI-030/031); public risk banner mandatory when provider=public.
- **by_scenario** (2026-08-05): engine `ensure_by_scenario` — stub for domains without a split; snn_lif keeps generative `split`.

---

## NL-ADR-019 — North star: cover frontier strengths with our system + measured resource economy

**Status:** Accepted (2026-08-02)

**Context:** Founder clarified long-range intent: not clone Kimi/Grok; build a **distinct breed** (Synapse decide + Neurolab language + contour). Still want investor-credible path to large models and optional public client. Differentiator vs frontier scale race: **resource economy** from Synapse / SNN science, measured.

**Decision:**

1. **North star** (see `STRATEGY.md`): cover frontier capability *where it matters* with **our system**, win on **joule/watt/hardware/active-FLOPs** where science allows; stay architecturally unlike a monolith frontier LLM.  
2. **Lineage:** Tiny/suite (on-prem) → Mid → Large/MoE (own or client private cloud for buyers without DC) → optional public client as separate SKU (contour remains default).  
3. **Non-goals:** frankenstein «best of Kimi+Grok» weights; chasing Synapse oracle gap with bigger GGUF; GTM claims of frontier parity without eval + CARD + resource proxies.  
4. Agents cite this ADR + `STRATEGY.md` when framing Mid/Large, public SaaS, or investor/grant narrative.

**Consequences:**

- Scale still gated by `SCALE-PLAN.md` (Tiny quality before Mid cluster spend).  
- Synapse stays decide/escalate owner; Brain explains — do not collapse into one chat model.  
- Delivery modes A/B/C stay under `CONTOUR-EGRESS.md` (public LLM default off).

---

## NL-ADR-020 — Open D1 `neuro_chip` (rough estimate, not fab)

**Status:** Accepted (2026-08-02)

**Context:** D0 `snn_lif` + CS-P03 Port + Commercial Synapse Gate are green. MVP scheduled D1 after D0 demo as map/estimate toward neuromorphic targets. Risk: agents invent PDK/tape-out scope.

**Decision:**

1. Open domain plugin **`neuro_chip`** in `sandbox/src/closed_sandbox/domains/neuro_chip/`.  
2. v0.1+ named estimate targets: start with **`generic_neuromorphic_v0`**; FPGA class via **NL-ADR-021** (`fpga_snn_lite_v0`).  
3. Optional `[chip].source_metrics` from prior `snn_lif` run; else topology heuristic.  
4. **Explicit non-goals:** ASIC/PDK/GDSII, vendor SDK export, claiming measured silicon Joules, Akida/Loihi-accurate models (later named targets = new coeffs + ADR note).  
5. Example: `examples/chip_estimate_v0/`.

**Consequences:**

- Amends NL-ADR-012 “v0 only D0” — D0 remains default demo; D1 is additive plugin.  
- Ask prompts for `neuro_chip` must refuse inventing process nodes / GDSII.  
- FPGA named estimate: see **NL-ADR-021** (not bitstream).

---

## NL-ADR-021 — Named FPGA estimate target `fpga_snn_lite_v0`

**Status:** Accepted (2026-08-03)

**Context:** D1 opened with only `generic_neuromorphic_v0`. Next lever: named FPGA/SDK-class **estimate** without pretending Vivado/bitstream or vendor SDK.

**Decision:**

1. Add target **`fpga_snn_lite_v0`** (`chip_class=fpga`) with LUT/BRAM/DSP proxies + power/area/latency proxies.  
2. On FPGA runs, emit `chip_export` object; CLI writes `out/chip_export.json` (hook for later human vendor map).  
3. Example: `examples/chip_fpga_lite_v0/`.  
4. **Still out:** automatic bitstream, vendor SDK calls, claiming measured board Watts or official utilization %.

**Consequences:**

- Amends NL-ADR-020 §2 (“generic only”) — multiple named estimate targets allowed; each new vendor-accurate profile needs coeffs + ADR note.  
- Ask/contour must not invent Vivado reports from these proxies.

---

## NL-ADR-022 — Open D2 `biocompute` (digital GRN toy, wet-lab out)

**Status:** Accepted (2026-08-03)

**Context:** D0/D1 green. MVP lists D2 as digital biocompute (GRN / bacterial circuit abstractions). Must not imply in-house wet-lab.

**Decision:**

1. Open domain **`biocompute`** with kind **`boolean_grn_v0`**: discrete threshold GRN, synthetic majority-bit task.  
2. Metrics: accuracy/f1 + `bio_*` (`bio_n_genes`, `bio_n_edges`, `bio_resource_proxy`, disclaimer). `spike_count=0`; `synops` = regulatory ops on test.  
3. Example: `examples/biocompute_grn_v0/`.  
4. **Out:** culture, organoids, DNA synthesis, claiming ATP Joules or wet measurements.

**Consequences:**

- Same platform core as D0/D1; ask facts refuse wet-lab invention.  
- Richer GRN / DNA-computing toys = later kinds under this domain + STATUS note.

**Close note (2026-08-03):** D2 **v0.1 complete** — `boolean_grn_v0` + example + tests; richer kinds deferred. Next domain track = D3.

---

## NL-ADR-023 — Open D3 `biosignal` (synthetic ECG/EEG → spikes)

**Status:** Accepted (2026-08-03)

**Context:** D2 v0.1 closed. MVP D3 = event-encode biosignals → SNN/classifier. Must not ship clinical/medical claims.

**Decision:**

1. Open domain **`biosignal`** with kinds **`synthetic_ecg_v0`** / **`synthetic_eeg_v0`**.  
2. Encode: **`threshold`** spike train; classify with small LIF (reuse `snn_lif.lif`).  
3. Example: `examples/biosignal_ecg_v0/`.  
4. **Out:** clinical devices, diagnostic claims, real patient PHI, wet electrodes as product.

**Consequences:**

- Disclaimer on every run (`signal_disclaimer`).  
- Real MEA/partner ingest = later kind + data contract, not this ADR.

---

## NL-ADR-024 — Open D4 `hybrid` (bio front → silicon SNN)

**Status:** Accepted (2026-08-03)

**Context:** D0–D3 exist. MVP D4 = composition: bio-side front data + silicon SNN backend (CODE: hybrid = composition of plugins, not monolith).

**Decision:**

1. Open domain **`hybrid`**: `[front]` (reuse D3 synthetic ECG/EEG + threshold encode) → `[backend]` (`snn_lif` LIF classify).  
2. Example: `examples/hybrid_ecg_snn_v0/`. Metrics: `hybrid_pipeline` / `hybrid_front` / `hybrid_backend` + standard keys.  
3. **Out:** wet-lab, clinical claims, real-time vendor neuromorphic runtime, inventing measured bio-Joules.

**Consequences:**

- D4 is the first **cross-domain composition** proof; richer fronts (GRN events, partner MEA files) = later kinds.  
- UI two-pane still needs separate ★ (not this ADR).

---

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

---

## NL-ADR-026 — STATUS as sole focus source + monthly session-log rotation

**Status:** Accepted (2026-08-08)

**Context:** Current focus was duplicated in `AGENTS.md` §6, `docs/ARCHITECTURE.md` §6, and elsewhere with stale numbers (dead `/16` scale, Tiny LoRA shown as active work against `STATUS.md` "Pause Tiny LoRA sheet chase"). The session log in `STATUS.md` had grown to 449 lines / 59 entries, making the file hard to scan and the agent ritual impossible to follow where it referenced non-existent STATUS sections ("Done / In progress / Backlog").

**Decision:**

1. **`STATUS.md` is the sole source of current focus** — §Summary + §Next only. `AGENTS.md` §6 and `docs/ARCHITECTURE.md` §6 are pointers to this file, not copies of focus text or scores.
2. **Session log rotation** — entries older than the current calendar month move verbatim to `docs/SESSIONS-<YYYY-MM>.md` without editing text. Rule lives in `AGENTS.md` §4 Конец; first archive: `docs/SESSIONS-2026-07.md` (32 entries ≤2026-07-31).
3. **Ritual alignment** — agent start step 3 reads `STATUS.md` §Summary + §Next; end-of-session updates §Summary / §Ladder / §Next and the session log only in `STATUS.md`.

**Consequences:**

- One place to update focus per session; drift between canon docs eliminated for AGENTS / ARCHITECTURE.
- `STATUS.md` shrinks as archives accumulate (449 → 248 lines after July rotation); `docs/INDEX.md` lists session archives.
- Stale "current" claims in `README.md` §Треки and `docs/SCALE-PLAN.md` §3 were flagged at acceptance time — separate fix, not part of this ADR.

---

## NL-ADR-027 — Outward numbers quoted only from `CLAIMS.md`

**Status:** Accepted (2026-08-08)

**Context:** Honest caveats existed inside the repo (`PILOT-CONTOUR-CHAT.md`, eval reports) but outward-facing docs (`INVESTOR-NORTH-STAR.md` § Proof points) quoted naked numbers (`20/20` without runtime share, `f1 ≈0.93` without spread). Manual `CARD.md` drifted from disk: missing SHA/LICENSE/date, `hammer` and `hammer2` byte-identical, empty raw-evidence dir for the flagship 20/20 run.

**Decision:**

1. **`docs/CLAIMS.md` is the only quotable source** for numbers in grants, SOW, investor decks, and publications — cited verbatim with its caveat. Rows marked `internal` do not go outward.
2. **Model vs model+runtime never merged** into one headline number; both may appear only as separate CLAIMS rows.
3. **Machine passport block** in `models/*/CARD.md` comes only from `scripts/gen_model_card.py` (SHA256, sizes, sidecar match, eval scores split model / model+runtime). `--check` gates drift; `MISSING` instead of guessing (e.g. upstream base LICENSE).
4. **New measured result** → new row in `CLAIMS.md` in the same session, or the number is not quotable outside the lab.

**Consequences:**

- Central registry (`CLAIMS.md`, 28 rows at acceptance) prevents over-promising; `python3 scripts/gen_model_card.py --check` keeps passports aligned with artifacts.
- `INVESTOR-NORTH-STAR.md` § Proof points still needs rewrite through CLAIMS IDs (C-02, C-20+C-21, C-40, C-11) — GTM wording, human track at acceptance time.
- Re-run of pilot 20/20 with saved raw answers remains required to make C-02 fully verifiable.

---

## NL-ADR-028 — Locked base must leave Qwen2.5-3B (licence); target 7B

**Status:** Accepted (2026-08-13). Human: «переезжаем». Supersedes NL-ADR-002.

**Context:**

- `Qwen2.5-3B-Instruct` is **`qwen-research`, non-commercial only**, and clause 2.a covers
  derivative works — so every LoRA merge and GGUF we ship inherits it, `hammer` included.
  Verified against the official model card: `docs/BASE-LICENSE.md`.
- NL-ADR-002 locked this base while two files in the repo asserted Apache-2.0. That was wrong,
  never checked, and stood for three weeks.
- `7B` / `14B` / `32B`-Instruct are Apache-2.0 in **both** the metadata field and the `LICENSE`
  body (checked, not assumed). `72B` is a different licence (`qwen`) and is not an escape route.
- Lab machine: **M1 Pro, 16 GB unified memory**. Disk was down to ~7 GB free; see
  consequence below — that part is now fixed and is no longer an argument.
- Our own recipe states `--load-in-4bit` is CUDA/QLoRA only, and Unsloth breaks Apple Silicon
  (`docs/TRAIN-TINY-LORA.md` §0, §2).
- Training data is **small**: 11 sets, 13–92 examples each, 456 total.

**Decision:**

1. Target locked base = **`Qwen2.5-7B-Instruct`** (Apache-2.0). Not 14B as the next step: 7B
   already removes the licence problem, and 14B Q4 inference (~9 GB) would crowd a 16 GB box.
2. Until a 7B line exists, the **3B line is research / evaluation only**. No current GGUF may be
   distributed commercially, and no claim of the right to do so (`CLAIMS.md` §7).
3. **Memory blocker is lifted for MLX 4-bit LoRA, not for the default PEFT path.**
   7B FP16 + activations still do not fit 16 GB, and `--load-in-4bit` remains CUDA-only.
   **MLX probe 2026-08-13 (wave 3 / M):** `mlx_lm lora` on
   `mlx-community/Qwen2.5-7B-Instruct-4bit` measured **peak 5.022 GB** (1 iter, batch 1,
   seq 512, grad-checkpoint) on this M1 Pro. Details: `docs/MLX-7B-PROBE.md`.
   Train→GGUF recipe: `scripts/train_mlx_lora.py` + `docs/TRAIN-TINY-LORA.md` § MLX.
   `mlx_lm fuse --export-gguf` does **not** support `qwen2`; export is fuse `--dequantize`
   then llama.cpp `convert_hf_to_gguf.py` + `llama-quantize`. Fallbacks (CUDA 24 GB QLoRA,
   larger Mac) stay if fuse/dequantize OOMs on 16 GB.
4. **Disk is no longer an argument** — see consequences.
5. Re-collect the ladder on 7B with `scripts/score_agent_eval.py` at temperature 0 with repeats.
   **Carry no 3B number across** — a new base means a new baseline, not a rebased comparison.

**Consequences:**

- Every ladder number resets. `C-01`…`C-06` in `CLAIMS.md` become historical and tied to a
  research-only base; they stay quotable as lab history, not as product capability.
- The cheap part is data: 456 examples already curated, no new labelling. The cost is venue plus
  re-eval, and re-eval is now largely automated (track E scorer) — unlike the first climb.
- Compute is small: 40–90 examples × 2 epochs per set on MLX (probe ~0.25 it/s). GPU rental is
  not required for LoRA. Fuse+dequantize of 7B FP16 on 16 GB unified memory is the remaining
  risk for GGUF export.
- Existing 3B GGUFs (`hammer` and the rest) stay on disk as **research-only history**. They are
  not the locked base and must not ship commercially. New quotable scores start at 7B; do not
  rebase 3B 17/20 onto 7B.
- `outpost-tiny-hammer2.Q4_K_M.gguf` is byte-identical to `hammer` (`3a712954…`; all other
  eleven Q4 artifacts hash distinctly, so the ladder is otherwise real). Resolve that duplicate
  before any re-climb so the new ladder does not inherit a phantom rung.
- **Disk, done 2026-08-08:** `artifacts/` held **216 GB**, of which only ~26 GB was irreplaceable
  (12 Q4 GGUFs, 19 LoRA adapters at ~125 MB each, base). Deleting `runs/*/trainer` — HF trainer
  checkpoints, the scaffolding rather than the output — freed **84 GB**, taking free space from
  6.6 GB to 91 GB. Two runs had no `adapter/` dir and kept their only weights inside those
  checkpoints (`20260719-085839`, `20260719-mps-v1.1-nan12e4`); both were copied out to
  `adapter-rescued/` with provenance before deletion. Verified after: `hammer` still hashes
  `3a712954…`, 19 adapters and 19 `NOTES.md` intact.
- Still reclaimable if ever needed: `artifacts/hf/` (63 GB) and `artifacts/*.f16.gguf` (40 GB) are
  regenerable from adapter + `merge_tiny_lora.py`, at the cost of an FP16 base download and merge
  time. Not deleted, since 91 GB is already ample for a 7B move.

