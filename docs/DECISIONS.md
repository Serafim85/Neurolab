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
