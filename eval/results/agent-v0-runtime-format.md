# agent-v0 — LIVE hn + `[agent_format]` v2 → **20/20**

| Field | Value |
|---|---|
| **Date** | 2026-08-01 |
| **Daemon** | Commercial `target/release/sovereignd` (rebuilt into project `target/`, Aug 1) |
| **GGUF** | `artifacts/outpost-tiny-agent-hn.Q4_K_M.gguf` |
| **Config** | `config/sovereign.agent-format.toml` · `:8102` · `[agent_format] enabled = true` · guard **off** |
| **Raw** | `eval/results/raw/agent-v0-live-format-20260801/` |
| **Score** | **20 / 20** |

> Orthogonal to pilot hammer2 + contour_guard **20/20** on `prompts.ru.jsonl`.

## Score table

| id | Score | Source |
|---|---:|---|
| `tool_json` | 2 | model |
| `tool_json_args` | 2 | model |
| `plan_steps` | 2 | runtime `agent_plan_steps_airgap` |
| `code_lite` | 2 | model |
| `refuse_public` | 2 | model |
| `schema_extract` | 2 | model |
| `self_check` | 2 | model (hn) |
| `budget_sentences` | 2 | runtime `agent_budget_sentences` |
| `router_hint` | 2 | model |
| `plan_tool_mix` | 2 | runtime `agent_plan_label` |
| **Total** | **20** | |

## Note

Earlier live miss was a **stale binary** (`target/release/sovereignd` from Jul 23); sandbox `CARGO_TARGET_DIR` hid the rebuild. Fix: build with `CARGO_TARGET_DIR=$PWD/target`.
