# North star — build ladder (develop now)

> **Status:** living (2026-08-02) · NL-ADR-019  
> **Narrative:** [`STRATEGY.md`](STRATEGY.md) · investor excerpt: [`INVESTOR-NORTH-STAR.md`](INVESTOR-NORTH-STAR.md)  
> **Rule:** one lever per session · measure before/after · no Commercial runtime features in this repo

---

## 1. What “develop” means under the north star

Ship artifacts that prove:

1. **Breed** — Synapse decide ≠ Neurolab language ≠ Outpost runtime  
2. **Capability cover** — chat / agent / escalate / studio where buyers need them  
3. **Resource economy** — quality under spike/synops/budget (and later joule proxies)

Not: pretrain a Kimi-class model in this quarter.

---

## 2. Phases

| Phase | Focus | Lab owns | Commercial owns | Exit |
|---|---|---|---|---|
| **P0** | Lock narrative + economy in reports | docs + sandbox report economy block | — | ADR-019 + investor one-pager + `quality_per_kspike` ✅ |
| **P1** | Contour product harden | sandbox UI next ★/Port; ask smoke | Gate: explain + audit per handoff | SOW-ready Synapse explain |
| **P2** | Capability cover without size chase | agent eval keep; optional suite expert | agent_format default-on if promoted | sticky formats closed in runtime |
| **P3** | Mid when Tiny ceiling proven | Mid escalate / chat eval + CARD | load Mid on dc profile | NL-ADR for Construct `chat`→Mid |
| **P4** | Large / private cloud delivery | pack + passport | cloud contour B allowlist | buyers without own DC |
| **P5** | Public client SKU | model behavior contour-safe | consumer app | brand funnel; contour still default |

Gates for P3+: [`SCALE-PLAN.md`](SCALE-PLAN.md) §7 (Tiny quality, real task ceilings, hardware, human OK).

---

## 3. Now — ranked Lab backlog (pick one per session)

| # | Task | Why north star | Done when |
|---|---|---|---|
| **1** | Resource economy block in sandbox `report.md` (+ stress summary) | measure economy, grant annex | ✅ 2026-08-02 |
| **2** | Commercial Gate (explain + audit) | explain path to revenue | ✅ 2026-08-02 ADR-054 · smoke 3/3 · handoff implemented |
| **3** | Port next Sandbox screen after ★ (L01/L02/L04/L05) | product studio | FR + parity yaml |
| **4** | Optional Synapse specialist lift (not bigger GGUF) | breed stays Synapse-owned | +pp on class with CARD note |
| **5** | Mid escalate re-bench (ADR-016) only if P1 Gate blocked by Tiny ceiling | capability cover | measured Δacc vs stub |

Paused: Tiny LoRA sheet chase (plateau; runtime closed agent gaps).

---

## 4. Resource economy — definition v0 (Lab)

From existing sandbox metrics (no invented bio-joules):

| Proxy | Meaning |
|---|---|
| `spike_count` / `synops` | event activity cost |
| `budget_ok` | stayed inside declared neuron/synapse/spike budget |
| `f1` or `accuracy` | task quality |
| **`quality_per_kspike`** | `1000 * primary_quality / max(spike_count, 1)` |
| **`wall_ms`** | wall-clock cost of run |

v1 later: explicit mJ estimate only with cited model + ADR (see Closed Sandbox canon — no fake Joules).

---

## 5. Anti-patterns while building

- Collapsing Synapse into “just prompt a bigger LLM”  
- Starting Large/public client before Mid gate + measured economy story  
- Mixing EU grant decks with unverified STATUS claims  
- Implementing `sovereignd` features in neurolab

---

## 6. Session checklist

1. Read `STATUS.md` Next — take **one** row from §3 above.  
2. Baseline metric → change → re-eval.  
3. Update STATUS Session log + CARD/results if model.  
4. If delivery mode / scale step changes → ADR.
