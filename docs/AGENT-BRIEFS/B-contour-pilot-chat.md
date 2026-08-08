# Brief B — Contour pilot chat (hammer2 + guard)

**Track:** Ship / demo packaging for contour chat  
**Primary repo:** `/Users/valentin/Projects/neurolab`  
**Read first:** `AGENTS.md` · `STATUS.md` · `docs/DECISIONS.md` · `docs/CONTOUR-EGRESS.md`  
**Evidence:** `eval/results/tiny-hammer2-plus-guard.md` · `config/sovereign.tiny-hammer.toml` · `config/sovereign.sandbox-ask.toml`  
**Commercial (read-only unless smoke needs it):** `~/Projects/AI-Platform-Vision` — contour_guard / ADR-047 context if present  

---

## Mission

Make **hammer2 + contour_guard** ready as the **pilot contour chat** story: clear docs, smoke path, what to say in demo.  
**Do not** chase new Tiny LoRA for sheet scores (STATUS: pause Tiny LoRA chase). Quality bar stays hammer2 + guard **20/20**.

---

## Do exactly

### 1. Pilot pack doc

Create `docs/PILOT-CONTOUR-CHAT.md` (or update if a similar doc exists) covering:

| Section | Content |
|---|---|
| What ships | GGUF path `artifacts/outpost-tiny-hammer.Q4_K_M.gguf` + `[contour_guard] enabled = true` |
| Score | 20/20 with guard; 17/20 model alone — cite eval results |
| How to run | Lab config `config/sovereign.tiny-hammer.toml`; binary from Commercial `target/release/sovereignd`; port note |
| Demo script | 5–8 prompts: RU contour Qs, refuse public LLM, format discipline, short code; expected behavior |
| Guard | What guard covers vs what model covers (honest) |
| Not claimed | Not Grok-level; not Mid; not customer PII train |
| Sandbox ask | Link `CLOSED-SANDBOX-VERIFY.md` + `sovereign.sandbox-ask.toml` for ask↔Outpost |

### 2. Smoke checklist

Add or extend a short verify section (in that doc or `eval/results/pilot-contour-smoke.md`):

```text
[ ] GGUF present (path + size note; do not commit GGUF)
[ ] sovereignd boots with tiny-hammer.toml
[ ] model_loaded true
[ ] contour_guard on
[ ] 3 canned prompts pass (refuse public / formal format / happy path)
```

If you can run smoke on this host (Metal/GPU), record results. If not, mark **manual host required** and leave checklist for human.

### 3. CARD / STATUS hygiene

- Ensure `models/outpost-tiny/CARD.md` (or hammer card if separate) mentions hammer2 + guard demo bar — **small edit only**.  
- Do **not** promote micro/diverse.  
- Optional: if Commercial has DEMO-VERIFICATION doc, add a **pointer** from neurolab doc (do not invent Commercial GTM claims).

### 4. Config sanity

- Confirm `config/sovereign.tiny-hammer.toml` has contour_guard and correct model path comments.  
- Fix only broken comments/paths; no architecture thrash.

---

## Forbidden

- New LoRA train / dataset expansion “to beat 20/20”  
- Changing locked base away from Qwen2.5-3B  
- Promising Mid / Grok in pilot wording  
- Implementing Outpost runtime features in neurolab  
- Committing weights  

---

## Definition of Done

- [ ] Pilot doc exists and is linkable from INDEX / AGENTS map if you touch INDEX  
- [ ] Smoke checklist present (run or marked host-only)  
- [ ] CARD note consistent with STATUS ladder  
- [ ] `docs/AGENT-BRIEFS/results/B.md` written  

---

## Result file

`/Users/valentin/Projects/neurolab/docs/AGENT-BRIEFS/results/B.md`:

- files changed  
- smoke: ran / skipped + why  
- demo one-liner for human  
- next step (Commercial pack / customer wording — human)

**Do not** full-rewrite `STATUS.md`.
