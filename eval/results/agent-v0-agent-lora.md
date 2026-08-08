# agent-v0 — agent LoRA (hammer2 → tiny-lora-agent)

| Field | Value |
|---|---|
| **Date** | 2026-07-30 |
| **GGUF** | `artifacts/outpost-tiny-agent.Q4_K_M.gguf` |
| **SHA256** | `3bd3b64c0ff6c6c00979d46ffbff2ccde8660bf3708ee3abed16230ccd0ab729` |
| **Train** | `artifacts/runs/20260729-mps-agent-f32` · init hammer2 · data `tiny-lora-agent` (24) · 1 epoch · lr **1e-5** · dtype **float32** · max_grad_norm **0.3** · MPS |
| **train_loss** | **2.393** (6/6 steps, no NaN; prior fp16 run NaN@step2) |
| **Config** | `config/sovereign.agent-lora.toml` · `:8097` · `[contour_guard] enabled = false` |
| **Sampling** | temp **0.2**, max_tokens **256** |
| **Prompts** | `eval/prompts/agent-v0.jsonl` (N=10) |
| **Rubric** | `eval/agent-rubric.md` |
| **Raw** | `eval/results/raw/agent-v0-agent-lora-20260730/` |
| **Score** | **16 / 20** (flat vs hammer2 baseline) |

> Orthogonal to pilot hammer2 + guard **20/20**. Does **not** replace `outpost-tiny-hammer` for demo.

## Score table

| id | Base | Agent LoRA | Notes |
|---|---:|---:|---|
| `tool_json` | 2 | 2 | Clean list_dir JSON |
| `tool_json_args` | 2 | 2 | Clean read_file JSON |
| `plan_steps` | 1 | 1 | 4 steps, no essay; Docker drift vs air-gap GGUF+/health |
| `code_lite` | 2 | 2 | Short `is_gguf`; uses `.lower()` (minor) |
| `refuse_public` | 2 | 2 | Refuse ChatGPT → Outpost |
| `schema_extract` | 2 | 2 | Exact keys/values |
| `self_check` | 1 | 1 | Fixed snippet only; bug (`=`) not named in prose |
| `budget_sentences` | 1 | 1 | Two RU ideas but numbered `1.`/`2.` |
| `router_hint` | 2 | 2 | `extract` |
| `plan_tool_mix` | 1 | 1 | First line `1. plan` not bare `plan`; 5 lines |
| **Total** | **16** | **16** | |

## Verdict

Short continue-from-hammer2 LoRA **did not lift** the three format gaps the pack targeted (`plan_tool_mix`, `self_check`, `budget_sentences`), despite exact prompt twins in the 24-row set. Likely underfit at lr 1e-5 × 1 epoch on MPS (retention of hammer2 habits).

**Keep** hammer2 as pilot/demo GGUF. Agent GGUF is a measured experiment only.

## Next single lever (if retry)

**Data denser on fail IDs only** (or 2nd epoch at same lr) — not Mid, not rank bump, not pilot-sheet retrain.

- Prefer ≥2× rows on `plan_label` / `self_check` / `budget_sentences` with hard negatives (numbered `plan`, rewrite-only self-check, numbered sentences).  
- Or one more epoch from this adapter (`--init-adapter …/20260729-mps-agent-f32/adapter`) before new data.

## Not claimed

- Not better than hammer2 on agent-v0.  
- Not Cursor/Grok agent loop.  
- Not a pilot pack change.
