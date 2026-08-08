# Brief C — Cursor-like agent capability (eval + one lever)

**Track:** Move Tiny toward **agent/tool behavior** (Cursor-oriented), not size chase  
**Primary repo:** `/Users/valentin/Projects/neurolab`  
**Read first:** `AGENTS.md` · `STATUS.md` · `docs/INTELLECTUAL-CANON.md` §2–3 (post-train, test-time, agents/tools) · `docs/CONSTRUCT.md` · `docs/GOALS.md` §3.1 · `docs/TRAIN-TINY-LORA.md`  
**Orient:** Cursor Grok 4.5 = model + tool loop + product. **This brief = model-side formats only.** Runtime tool-loop stays Commercial Outpost / Pharos.

---

## Mission

1. Define a **small agent rubric** (what “Cursor-like” means for Outpost-Tiny).  
2. Score **hammer2 baseline** on that rubric (or mark prompts ready if daemon unavailable).  
3. Optionally prepare **one** data lever (messages JSONL draft) for tool/plan/JSON gaps — **do not** run long GPU train unless clearly cheap and brief allows; default = **data + eval only**.

---

## Do exactly

### 1. Spec: agent eval

Create `eval/agent-rubric.md` + prompts file e.g. `eval/prompts/agent-v0.jsonl` or `.md` sheet with **8–12 items** covering:

| Capability | Example ask | Pass criteria |
|---|---|---|
| Tool JSON | emit `{"tool":"...","args":{...}}` only | valid JSON, no prose wrap |
| Plan steps | 3–5 numbered steps | no essay; ordered |
| Code-lite | small util / path check | runs-in-head correctness, short |
| Refuse public LLM | contour refuse | matches CONTOUR-EGRESS spirit |
| Schema extract | fields → JSON | keys exact |
| Self-check | spot error in snippet | concrete fix, not vibes |
| Multi-step brief | given constraints, stay in budget tokens | ≤N sentences if asked |
| Router hint | choose extract vs chat | label only |

Keep RU + EN mix OK; prefer RU for contour realism.

Scoring: simple 0/1 or 0–2 per item; total / max. Document sampling: temp 0.2, max_tokens as needed.

### 2. Baseline measure

Against **hammer2** (`artifacts/outpost-tiny-hammer.Q4_K_M.gguf`) via existing lab smoke path / sovereignd if available.

Write `eval/results/agent-v0-hammer2-baseline.md`:

- date, config, score table  
- top 3 failure modes  
- recommended **single** lever (data only vs Mid later — recommend, don’t start Mid)

If cannot run inference: still ship rubric + prompts; result says **BLOCKED: host inference**.

### 3. Optional data lever (only if baseline ran OR failures are obvious from rubric design)

- Draft `datasets/tiny-lora-agent/STATS.md` + `train.messages.jsonl` with **≤30** high-quality examples targeting the worst gaps.  
- Follow existing dataset style (`datasets/tiny-lora-micro/` as pattern).  
- **Do not** merge/train/export GGUF in this brief unless human already has a one-command recipe and you verify it finishes quickly — prefer stop at data.

### 4. Construct note

Short note in `eval/agent-rubric.md` or `docs/CONSTRUCT.md` (tiny subsection / link only): future skills tags e.g. `tool_json`, `plan` on chat slot — **no runtime implementation**.

---

## Forbidden

- “Replace Grok” claims  
- Arch-MoE / Mid base change without ADR + human  
- Implementing agent shell / tool runtime in neurolab  
- Five experts at once  
- Touching Design Studio / Commercial UI  
- Conflict with Brief B: **do not** change pilot hammer2 promotion story; agent rubric is additive  

---

## Definition of Done

- [ ] Rubric + prompts exist  
- [ ] Baseline result file (scored or BLOCKED)  
- [ ] Optional small dataset **or** explicit “data deferred” with reason  
- [ ] `docs/AGENT-BRIEFS/results/C.md` written  

---

## Result file

`/Users/valentin/Projects/neurolab/docs/AGENT-BRIEFS/results/C.md`:

- score or blocked  
- top gaps  
- recommended next single lever for human  
- files changed
