# Brief C — result

**Track:** Cursor-like agent capability (eval + one data lever)  
**Date:** 2026-07-29  
**Status:** Done

## Score

**hammer2 model-only: 16 / 20** on `eval/prompts/agent-v0.jsonl`  
(temp 0.2 · `config/sovereign.agent-eval.toml` · contour_guard **off** · raw `eval/results/raw/agent-v0-hammer2-20260729-181042/`)

Not BLOCKED — inference available on host.

Orthogonal to Brief B: pilot remains hammer2 + guard **20/20** on contour sheet; agent rubric is additive.

## Top gaps

1. Hybrid `plan` label + numbered steps (`plan_tool_mix`)  
2. Self-check returns rewrite without naming the bug  
3. Soft sentence/budget discipline (`budget_sentences` numbering; weak `plan_steps` content)

Strong already: tool JSON, schema extract, code-lite, router label, model-side refuse_public.

## Recommended next single lever (human)

**Data → short LoRA** on `datasets/tiny-lora-agent/` (24 messages), then re-score agent-v0 only.  
Do **not** Mid, do **not** retrain for pilot contour sheet, do **not** implement agent shell in neurolab.

## Files changed

| Path | Role |
|---|---|
| `eval/agent-rubric.md` | Agent rubric + Construct skills note |
| `eval/prompts/agent-v0.jsonl` | 10 prompts |
| `eval/results/agent-v0-hammer2-baseline.md` | Scored baseline |
| `config/sovereign.agent-eval.toml` | hammer2 :8097, guard off (lab agent eval only) |
| `datasets/tiny-lora-agent/STATS.md` | Pack stats |
| `datasets/tiny-lora-agent/train.messages.jsonl` | 24 SFT examples |
| `docs/CONSTRUCT.md` | Tiny skills-tag link (no runtime) |
| `docs/AGENT-BRIEFS/results/C.md` | this file |

## DoD

- [x] Rubric + prompts (10 items, 8–12 band)  
- [x] Baseline result scored (not BLOCKED)  
- [x] Optional small dataset shipped  
- [x] This result file  

**No commit** (per brief).
