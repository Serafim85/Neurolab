# Synapse Gate — SOW / GTM wording (human gate)

> **Status:** **Approved** (2026-08-03) · human OK  
> **Evidence:** Commercial ADR-054 · smoke 3/3 · Lab ask 3/3 · specialist ≈0.864  
> **Related:** [`COMMERCIAL-GATE-HANDOFF.md`](COMMERCIAL-GATE-HANDOFF.md) · [`SYNAPSE-BRIDGE.md`](SYNAPSE-BRIDGE.md) · Commercial `docs/DECISIONS.md` ADR-054

Agents **may** reuse §3–§5 in pilot/SOW drafts. Still respect §2 forbidden list.
---

## 1. What is proven (may cite)

| Claim | Evidence |
|---|---|
| Synapse owns escalate *when* + class (`specialist`) | SYN-ADR-008 · E5 bench specialist ≈ **0.864** |
| Outpost explains escalate in NL; does **not** fix `class_id` | ADR-054 · CANONICAL FACTS · smoke roles 3/3 |
| Calls are audited (`synapse.escalate.received` / `synapse.brain.explain`) | Gate audit JSONL · flag default **off** until enable in config |
| Contour-safe path (local GGUF; no silent public LLM) | `CONTOUR-EGRESS` · hammer2 demo config |
| Lab Closed Sandbox can import Synapse KPIs and ask | `synapse_import` · ask report 2026-08-01 |

---

## 2. Forbidden (do not write in SOW / deck / site)

- «LLM чинит class / заменяет Synapse»  
- «Synapse chat» / «нейросеть-чат вместо Tiny»  
- «Measured silicon Joules / ATP / clinical ECG diagnosis» from Brain or sandbox toys  
- «Frontier parity / better than GPT» without separate eval + CARD  
- «Gate on by default in production» — default is **off** until SOW enables it  
- Oracle gap closed / 100% class accuracy  
- Bio wet-lab or fab/tape-out as shipped product  

---

## 3. Suggested one-liner (RU)

> Outpost принимает escalate от Synapse, **объясняет** решение оператору на локальном GGUF и **пишет audit**; класс на escalate задаёт Synapse (`specialist`), не LLM.

EN:

> Outpost consumes Synapse escalate payloads, **explains** them in-contour on a local GGUF, and **audits** the call; class repair stays with Synapse (`specialist`), not the LLM.

---

## 4. Suggested SOW scope bullet (pilot)

**In scope**

1. Enable `[synapse_bridge]` on agreed Outpost contour (air-gap / on-prem).  
2. Accept BRAIN-BRIDGE escalate JSON → NL explain (hammer2 or locked pilot GGUF).  
3. Emit audit events for escalate received / explain / explain_failed (metadata; no full prompt by default).  
4. Acceptance: fixture escalate + three role questions pass (class owner / escalate_rate / oracle_accuracy).  

**Out of scope (this SOW)**

- LLM as class fixer · Mid/Large as default chat · public SaaS egress · UI badge (optional follow-up) · Synapse accuracy chase beyond current specialist bar  

---

## 5. Investor / grant sentence (safe)

> We demonstrate a **split breed**: Synapse decides cheaply on events; Outpost explains and audits in a closed contour — without asking a chat model to own classification.

---

## 6. Sign-off

| Field | Value |
|---|---|
| Human | OK (chat 2026-08-03) |
| Date | 2026-08-03 |
| Decision | ☑ **OK Gate wording** |

**Approved.** Agents may reuse §3–§5 in pilot drafts. Engineering default remains flag-off on generic configs; **named pilot** `sovereign.pilot-contour-gate.toml` enables `[synapse_bridge]` (verified smoke 3/3, 2026-08-05).
