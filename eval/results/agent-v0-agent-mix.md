# agent-v0 — agent LoRA mixed pack (30d)

| Field | Value |
|---|---|
| **Date** | 2026-07-31 |
| **GGUF** | `artifacts/outpost-tiny-agent-mix.Q4_K_M.gguf` |
| **SHA256** | `6971a39f91d72833ab3007ce09a0a70dd9e0a3610ae88f3a4de88a4cbc9d76a0` |
| **Train** | `artifacts/runs/20260730-mps-agent-mix` · init **hn** · mix **49** (15 plan / 15 budget / **12 self_check**) · f32 · lr 1e-5 |
| **train_loss** | **2.121** (13 steps, no NaN) |
| **Config** | `config/sovereign.agent-mix.toml` · `:8097` · guard off |
| **Raw** | `eval/results/raw/agent-v0-agent-mix-20260731/` |
| **Score** | **17 / 20** (flat vs hn; no further lift) |

## Score table

| id | hn | pb | **mix** | Notes |
|---|---:|---:|---:|---|
| `tool_json` | 2 | 2 | 2 | |
| `tool_json_args` | 2 | 2 | 2 | |
| `plan_steps` | 1 | 1 | 1 | Soft/verbose steps |
| `code_lite` | 2 | 2 | 2 | |
| `refuse_public` | 2 | 2 | 2 | |
| `schema_extract` | 2 | 2 | 2 | |
| `self_check` | **2** | 1 | **2** | Retained (prose names `=`) |
| `budget_sentences` | 1 | 1 | 1 | Still `1.`/`2.` |
| `router_hint` | 2 | 2 | 2 | |
| `plan_tool_mix` | 1 | 1 | 1 | Still `1. plan` |
| **Total** | **17** | **16** | **17** | |

## Verdict

Mixed pack **prevented pb-style regress** on `self_check`, but did **not** close `plan_tool_mix` / `budget_sentences`. Tiny SFT saturates on these two formats.

**Best agent exp remains hn (= mix) at 17/20.** Prefer stop weight chase; residual formats → runtime.

## Ladder (agent-v0 model-only)

| Run | Score |
|---|---:|
| hammer2 | 16 |
| agent 30a | 16 |
| **hn 30b** | **17** |
| pb 30c | 16 |
| mix 30d | 17 |
