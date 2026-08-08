# Brief D — result · Brain ↔ Synapse router contract

**Date:** 2026-07-29  
**Status:** Done (docs/contract only · no commit · neurolab STATUS not rewritten)

---

## Contract one-liner

**Synapse decides fast/cheap on events (`fire`/`score`/`route`/`escalate`); Neurolab→Outpost GGUF owns language; Outpost Commercial loads/audits — Brain bridge v0 is contract only (SYN-ADR-008).**

---

## Files

### Synapse (`~/Projects/synapse`)

| File | Role |
|---|---|
| `docs/BRAIN-BRIDGE.md` | **SoT** — roles, call patterns, payloads, ownership, honesty |
| `docs/examples/brain-bridge-v0.toml` | Example junction (`synapse_first`, cascade3, hammer2 placeholder, timeouts) |
| `docs/DECISIONS.md` | **SYN-ADR-008** — Brain bridge v0 = contract only (+ E5 escalate lab probe) |
| `STATUS.md` | Done + Session log note for bridge contract |
| `AGENTS.md` | Doc map → BRAIN-BRIDGE + example |
| `docs/BOUNDARIES.md` | Pointer to BRAIN-BRIDGE |
| `docs/COMPOSE.md` | Escalate wrap note (aligned field names) |

Related lab probe (not Outpost chat): `export/e5-brain-escalate/` — when-to-call `escalate` + stub/oracle.

### Neurolab (`~/Projects/neurolab`)

| File | Role |
|---|---|
| `docs/SYNAPSE-BRIDGE.md` | Thin pointer → Synapse SoT |
| `docs/CONSTRUCT.md` §6.1 | Short junction note (no schema change / no NL-ADR) |
| `docs/INDEX.md` | Link to SYNAPSE-BRIDGE |
| `docs/AGENT-BRIEFS/results/D.md` | This result |

**Not done (by brief):** full `STATUS.md` rewrite · training · UI · Commercial SOW · commit.

---

## Open questions for human

1. Calibrate escalate `τ` on a **real** Outpost brain success curve (not E5 oracle).  
2. First Commercial Gate shape: sidecar vs tool call vs Construct skill?  
3. Later: add Construct `external_ensemble` skill (would need NL-ADR) — or keep pointer-only until Outpost consumes packs?

---

## Suggested next implementer

**Outpost Commercial Gate** — real Brain `/v1/chat` (or tool) consumer of Synapse `escalate` + structured context.  
Synapse keeps mock/oracle benches and the contract stable until that Gate exists. Lab mock wire is optional interim only.
