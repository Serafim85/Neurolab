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

**Status:** Accepted (2026-07-18)

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
