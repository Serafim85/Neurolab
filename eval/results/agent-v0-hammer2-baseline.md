# agent-v0 baseline — hammer2 (model-only)

| Field | Value |
|---|---|
| **Date** | 2026-07-29 |
| **GGUF** | `artifacts/outpost-tiny-hammer.Q4_K_M.gguf` (hammer2) |
| **SHA256** | `3a7129549bf19c69663c581741e917e8fadc5d40dedd99598eab31ad0b1f6e8c` |
| **Config** | `config/sovereign.agent-eval.toml` · `:8097` · `[contour_guard] enabled = false` |
| **Sampling** | temp **0.2**, max_tokens **256** |
| **Prompts** | `eval/prompts/agent-v0.jsonl` (N=10) |
| **Rubric** | `eval/agent-rubric.md` |
| **Raw** | `eval/results/raw/agent-v0-hammer2-20260729-181042/` |
| **Score** | **16 / 20** |

> Orthogonal to Brief B pilot sheet (hammer2 + guard **20/20** on `prompts.ru.jsonl`). This run measures **agent formats** without contour_guard canned paths.

## Score table

| id | Score | Notes |
|---|---:|---|
| `tool_json` | 2 | Clean `{"tool":"list_dir","args":{"path":"/data"}}` |
| `tool_json_args` | 2 | Clean read_file JSON w/ max_bytes |
| `plan_steps` | 1 | 4 steps, no essay; weak air-gap /health content |
| `code_lite` | 2 | Correct short `is_gguf` |
| `refuse_public` | 2 | Refuse ChatGPT + Outpost (model-side) |
| `schema_extract` | 2 | Exact keys/values; pretty JSON OK |
| `self_check` | 1 | Fixed code shown; bug not named in prose |
| `budget_sentences` | 1 | Two RU ideas but numbered `1.`/`2.` not bare sentences |
| `router_hint` | 2 | `extract` |
| `plan_tool_mix` | 1 | Steps present; first line was `1. plan` not `plan`; 5 lines |
| **Total** | **16/20** | |

## Top 3 failure modes

1. **Hybrid format / first-line label** — `plan_tool_mix` folds `plan` into a numbered list instead of bare label + ≤4 steps.  
2. **Self-check as rewrite** — returns corrected snippet without stating the concrete bug (`=` vs comparison).  
3. **Soft format discipline** — `budget_sentences` adds numbering; `plan_steps` drifts from `/health` air-gap intent.

Tool JSON and router/schema/code are already strong on hammer2 — do **not** overweight those in the next data pack.

## Recommended single lever

**Data only:** small SFT messages pack targeting format gaps (`plan_tool_mix`, `self_check` verbal fix, exact N-sentence / bare plan label). Draft: `datasets/tiny-lora-agent/` (≤30 rows).

- **Do not** start Mid / base change.  
- **Do not** retrain for pilot contour sheet (already 20/20 with guard).  
- Train/merge/export only if human green-lights a short recipe later.

## Not claimed

- Not Cursor/Grok-level agent loop.  
- Not runtime tool shell (Commercial).  
- Not a replacement for Brief B pilot pack.
