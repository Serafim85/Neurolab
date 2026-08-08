# Brief D — Brain ↔ Synapse router contract

**Track:** Document the junction between Neurolab “brain” (ANN/GGUF) and Synapse “synapse” (bio atoms / ensembles)  
**Primary repos:**  
- `/Users/valentin/Projects/synapse` (compose / charter / STATUS)  
- `/Users/valentin/Projects/neurolab` (Construct / GOALS — docs only)  

**Read first:**  
Synapse: `AGENTS.md` · `STATUS.md` · `docs/CHARTER.md` §3 Hybrid honesty · `docs/COMPOSE.md` · `docs/GATES.md`  
Neurolab: `docs/CONSTRUCT.md` · `docs/MICRO-MOE.md` · `docs/ARCHITECTURE.md` § Lab→Outpost · NL-ADR-006  

---

## Mission

Write a **stable cross-lab contract**: when Synapse decides / routes, when Neurolab chat/reasoning is called, what payloads look like, what is explicitly **not** promised.  
Docs + example manifest only. **No** new training, **no** Commercial SOW, **no** UI.

---

## Do exactly

### 1. Joint contract doc (pick one home + pointer)

**Preferred home:** `synapse/docs/BRAIN-BRIDGE.md`  
**Pointer in neurolab:** short `docs/SYNAPSE-BRIDGE.md` (or section link from CONSTRUCT) → synapse doc as SoT for bio side.

Must include:

#### Roles

| Layer | Owner lab | Responsibility |
|---|---|---|
| L0 atom / L1 ensemble | Synapse | fast/cheap decide: fire, score, route, energy proxies |
| Chat / plan / tools language | Neurolab → Outpost GGUF | language, deep reasoning, tool JSON |
| Product runtime | Outpost (Commercial) | load GGUF, audit, governor — **not implemented here** |

#### Call patterns

1. **Synapse-first cascade:** events → Synapse ensemble → if uncertain / needs language → call Outpost chat slot.  
2. **Brain-first with Synapse gate:** user text → Tiny chat → optional Synapse specialist for sensor/anomaly subtask.  
3. **Parallel (defer):** only document as future; do not invent.

#### Payload sketch (JSON-ish)

```text
Synapse → Brain request:
  { "reason": "uncertain"|"explain"|"plan", "score": 0.0-1.0, "route": "...",
    "context": { "metrics": {...}, "card_id": "..." } }

Brain → Synapse (optional):
  { "intent": "run_atom"|"ignore", "atom_id": "...", "args": {...} }
```

Align field names with Synapse COMPOSE (`fire`, `score`, `route`, `ok`) where possible.

#### Router ownership

| Question | Answer (decide and write) |
|---|---|
| Who owns rules-v0 for sensors? | Synapse |
| Who owns chat/tool router? | Neurolab Construct / Outpost agents.toml later |
| Can Synapse emit natural language? | **No** for H0–H1 — return structured; Brain verbalizes |
| Can Brain claim bio energy metrics? | **No** — cite Synapse CARD/metrics only |

### 2. Example manifest snippet

Add example file, e.g. `synapse/docs/examples/brain-bridge-v0.toml` or YAML:

- lists Synapse ensemble id (e.g. cascade3 / current S3 pack)  
- lists Neurolab slot `chat` → hammer2 path **as placeholder string**  
- `policy = synapse_first` or `brain_first`  
- fallbacks on timeout  

### 3. ADR notes

- Synapse: short SYN-ADR entry (or STATUS decision line) “Brain bridge v0 = contract only”.  
- Neurolab: optional NL-ADR stub **only if** Construct gains a formal `external_ensemble` skill — prefer thin pointer over big ADR if no schema change yet.

### 4. Honesty section

Explicit non-goals:

- Not replacing Outpost-Tiny with SNN chat  
- Not Grok-level reasoning in Synapse  
- Not Commercial pilot SOW from this doc  

---

## Forbidden

- Implementing bridge runtime in either lab “for real” beyond example docs  
- Changing Synapse S3 gate metrics / re-running full benches unless needed for a cite  
- Training / GGUF work (Brief B/C)  
- UI / Design Studio (Brief A)  
- GTM language  

---

## Definition of Done

- [ ] `BRAIN-BRIDGE.md` (synapse) complete  
- [ ] Neurolab pointer doc or CONSTRUCT link  
- [ ] Example manifest snippet  
- [ ] ADR/STATUS note on synapse side  
- [ ] `docs/AGENT-BRIEFS/results/D.md` in neurolab  

---

## Result file

`/Users/valentin/Projects/neurolab/docs/AGENT-BRIEFS/results/D.md`:

- contract one-liner  
- files in both repos  
- open questions for human (if any)  
- suggested next implementer (Outpost Gate vs lab mock)
