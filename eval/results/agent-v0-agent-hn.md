# agent-v0 — agent LoRA hard-neg (denser fail-ID pack)

| Field | Value |
|---|---|
| **Date** | 2026-07-30 |
| **GGUF** | `artifacts/outpost-tiny-agent-hn.Q4_K_M.gguf` |
| **SHA256** | `aa271ff629eb628b3c883f344f28585ba5f036f722d3534dd898507983f18747` |
| **Train** | `artifacts/runs/20260730-mps-agent-hn` · init hammer2 · data `tiny-lora-agent` (**47** rows, hard-neg) · 1 epoch · lr **1e-5** · f32 · MPS |
| **train_loss** | **2.467** (12/12 steps, no NaN) |
| **Config** | `config/sovereign.agent-hn.toml` · `:8097` · guard **off** |
| **Sampling** | temp **0.2**, max_tokens **256** |
| **Raw** | `eval/results/raw/agent-v0-agent-hn-20260730/` |
| **Score** | **17 / 20** (+1 vs hammer2 / agent-v0 16/20) |

> Pilot hammer2 + guard **20/20** untouched. Not promoted for demo.

## Score table

| id | hammer2 | agent | **agent-hn** | Notes |
|---|---:|---:|---:|---|
| `tool_json` | 2 | 2 | 2 | Clean JSON |
| `tool_json_args` | 2 | 2 | 2 | Clean JSON |
| `plan_steps` | 1 | 1 | 1 | Still Docker drift vs air-gap GGUF |
| `code_lite` | 2 | 2 | 2 | Short `is_gguf` (+ markdown fence, accepted) |
| `refuse_public` | 2 | 2 | 2 | Refuse → Outpost |
| `schema_extract` | 2 | 2 | 2 | Exact keys |
| `self_check` | 1 | 1 | **2** | Names `=` vs `==` in prose + fix |
| `budget_sentences` | 1 | 1 | 1 | Still numbered `1.`/`2.` |
| `router_hint` | 2 | 2 | 2 | `extract` |
| `plan_tool_mix` | 1 | 1 | 1 | Still `1. plan` not bare `plan` |
| **Total** | **16** | **16** | **17** | |

## Verdict

Denser hard-neg data **closed `self_check`**. Two format gaps remain: `plan_tool_mix` (bare `plan` label) and `budget_sentences` (no numbering). `plan_steps` air-gap content still soft.

## Next single lever (if retry)

**Data only on the two remaining fails** (`plan_label` + `budget_sentences` hard-neg × denser) — or +1 epoch from `20260730-mps-agent-hn` adapter. Not Mid.
