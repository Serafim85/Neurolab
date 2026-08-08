# Commercial Gate handoff — Synapse explain consumer + audit

> **Status:** **Implemented** in Commercial (2026-08-02) · ADR-054 · smoke 3/3  
> **Impl home:** `~/Projects/AI-Platform-Vision` (Outpost) — **not** neurolab  
> **Contract SoT:** `~/Projects/synapse/docs/BRAIN-BRIDGE.md` (v0.3 roles)  
> **Lab pointer:** [`SYNAPSE-BRIDGE.md`](SYNAPSE-BRIDGE.md) · build: [`NORTH-STAR-BUILD.md`](NORTH-STAR-BUILD.md) §3 #2

Handoff checklist below is the acceptance record. Lab still does not ship `sovereignd` features here.

---

## 1. One-liner

**Synapse decides** (when + class on escalate); **Outpost Brain explains** in natural language; **Outpost audits** the call. LLM must **not** repair `class_id`.

---

## 2. Recommended Gate shape (v1)

| Option | Verdict |
|---|---|
| **A. Escalate → chat context inject** | **Choose for v1** — Brain `/v1/chat` with structured Synapse payload in messages; no Construct schema change |
| B. Tool call `synapse_escalate` | Later — needs agents/tool loop productization |
| C. Construct `external_ensemble` skill | Later — needs NL-ADR + schema bump |
| D. Sidecar microservice | Avoid — blurs contour / two daemons |

**v1 flow:**

```text
Synapse ensemble (escalate=true)
  → payload §4.1 BRAIN-BRIDGE
  → Outpost Gate: validate → build chat messages → /v1/chat (slot chat / hammer2)
  → NL answer to operator / UI
  → audit JSONL: escalate + brain call metadata (not full prompt by default)
```

Policy default: **synapse_first** (events/metrics primary). `brain_first` deferred unless product asks.

---

## 3. Ownership (do not invert)

| Job | Owner |
|---|---|
| Cascade / escalate *when* | Synapse E5 |
| Class fix on escalate | Synapse **`specialist`** (default); `stage_vote` fallback |
| Explain / plan / NL | Outpost chat (Neurolab GGUF: hammer2) |
| Load GGUF, governor, audit | **Outpost Commercial** |
| Lab ask smoke / KPI import | Neurolab `sandbox/` (reference only) |

Evidence Lab already holds: specialist **0.8636**; ask roles **3/3** — `sandbox/reports/e5-roles-ask-20260801.md`.

---

## 4. Payload contract (consume, do not fork)

SoT fields: Synapse `BRAIN-BRIDGE.md` §4.1.

Minimum Outpost must accept:

```json
{
  "reason": "uncertain",
  "score": 0.42,
  "route": "cascade-hard",
  "fire": false,
  "ok": true,
  "escalate": true,
  "context": {
    "metrics": {},
    "card_id": "…",
    "atoms": {}
  }
}
```

| Rule | Detail |
|---|---|
| `escalate != true` | Gate must not call Brain for decide-only rows |
| `ok == false` | Degraded path: explain failure; do not invent metrics |
| `reason` | `uncertain` \| `explain` \| `plan` — shapes system prompt tone |
| Metrics | Cite only payload / CARD — **no invented Joules** |
| Class | If payload includes class/specialist fields, Brain **reports** them; never overrides |

Optional later: Brain → Synapse `run_atom` (§4.2) — **out of v1 Gate**.

---

## 5. Explain consumer — behavior DoD

Mirror Lab CANONICAL FACTS (`contour_ask` domain `synapse_import`):

1. Who fixes `class_id`? → **Synapse specialist** (or configured `class_fix`), **not** the LLM.  
2. What is `escalate_rate`? → fraction of uncertain rows — **not** accuracy, **not** another SNN.  
3. What is `oracle_accuracy`? → lab ceiling — **not** a product KPI.  
4. Answers cite payload metrics; refuse bio-joule invention.  
5. Contour-safe: no silent public LLM egress (`CONTOUR-EGRESS.md`).

**Acceptance prompts (Commercial smoke):** three questions above with a fixture escalate payload; expect role-correct answers on hammer2 (same bar as Lab ask 3/3).

Lab reference config: `config/sovereign.sandbox-ask.toml` · GGUF `artifacts/outpost-tiny-hammer.Q4_K_M.gguf`.

---

## 6. Audit DoD

Emit audit events (metadata; prompt body **off** by default — align Commercial audit policy):

| Event | Fields (min) |
|---|---|
| `synapse.escalate.received` | `card_id`, `reason`, `score`, `route`, `escalate`, `ok`, `ts` |
| `synapse.brain.explain` | `model_id`, `latency_ms`, `ok`, `reason`, `ts` |
| `synapse.brain.explain_failed` | `error_class`, `ts` |

Do **not** log full user/Synapse raw dumps to UI by default. Ops/audit screens may show counts + last reason.

---

## 7. Lab assets for the implementer

| Asset | Path |
|---|---|
| Contract SoT | `~/Projects/synapse/docs/BRAIN-BRIDGE.md` |
| Example junction TOML | `~/Projects/synapse/docs/examples/brain-bridge-v0.toml` |
| Escalate payload builder / E5 probe | `~/Projects/synapse/export/e5-brain-escalate/` |
| Roles ask report | `neurolab/sandbox/reports/e5-roles-ask-20260801.md` |
| Import example | `neurolab/sandbox/examples/synapse_e5_import/` |
| Ask system-prompt facts | `neurolab/sandbox/src/closed_sandbox/contour_ask.py` (`synapse_import`) |
| Lab Outpost ask config | `neurolab/config/sovereign.sandbox-ask.toml` |

---

## 8. Commercial implementation checklist

- [x] ADR in Commercial (**ADR-054**) — Gate scope = explain + audit, **not** class fix  
- [x] Config flag default **off** (`[synapse_bridge] enabled = false`) until SOW  
- [x] Named pilot enable: Commercial `config/sovereign.pilot-contour-gate.toml` (:8097) — Gate **on** (2026-08-05) · chat-only pilot `:8096` stays off  
- [x] Validate escalate JSON (reject / degrade on schema miss)  
- [x] Map payload → chat messages + CANONICAL FACTS system prefix  
- [x] Call existing chat inference path (`POST /v1/synapse/escalate` → backend)  
- [x] Audit events §6 wired (`synapse.escalate.received` / `synapse.brain.explain[_failed]`)  
- [x] Smoke: 3 role prompts pass — `./scripts/synapse-gate-smoke.sh` on `:8097`  
- [x] STATUS / DEMO note: Lab evidence cited; no GTM “Synapse chat” wording  
- [ ] Optional UI: show last escalate reason + “explained by Outpost” (not required for Gate v1 code)  
- [x] Human OK before pilot SOW language → [`SYNAPSE-GATE-SOW-WORDING.md`](SYNAPSE-GATE-SOW-WORDING.md) (**Approved** 2026-08-03)  

---

## 9. Explicit non-goals (v1)

- LLM as product class fixer on DVS escalate  
- Replacing Tiny with SNN chat  
- Mid escalate brain as default Construct `chat` (lab-only ADR-016 until new ADR)  
- Public client / zone C  
- SOW/GTM claims beyond STATUS Done  
- Implementing Gate inside neurolab or synapse repos  

---

## 10. Done when

1. ✅ Commercial ADR-054 + flag-off default.  
2. ✅ Fixture escalate → NL explain respects roles (3/3).  
3. ✅ Audit events in JSONL (`synapse.*`).  
4. ✅ Neurolab `SYNAPSE-BRIDGE.md` → **implemented**.  
5. ✅ Human OK — [`SYNAPSE-GATE-SOW-WORDING.md`](SYNAPSE-GATE-SOW-WORDING.md) **Approved** 2026-08-03  
6. ✅ Named pilot Gate-on — `sovereign.pilot-contour-gate.toml` · smoke **3/3** (2026-08-05)

---

## 11. Suggested first Commercial PR slice

1. Config + validate + chat inject + audit (no UI).  
2. Smoke script/test with frozen fixture JSON from Synapse export or Lab report.  
3. Docs: Commercial STATUS session + ADR.  

UI / SOW / Mid brain — separate PRs.
