# agent-v0 — agent LoRA plan+budget focus (30c)

| Field | Value |
|---|---|
| **Date** | 2026-07-30 |
| **GGUF** | `artifacts/outpost-tiny-agent-pb.Q4_K_M.gguf` |
| **SHA256** | `78ec7d7091c5f6fdd8bdbf501ac15c0a36fe049e4afb03128b4c186bc8b7af40` |
| **Train** | `artifacts/runs/20260730-mps-agent-pb` · init **agent-hn** · focus pack **46** (20 plan + 20 budget) · f32 · lr 1e-5 · 12/12 |
| **train_loss** | **2.289** |
| **Config** | `config/sovereign.agent-pb.toml` · `:8097` · guard off |
| **Raw** | `eval/results/raw/agent-v0-agent-pb-20260730/` |
| **Score** | **16 / 20** (−1 vs hn 17/20) |

## Score table

| id | hammer2 | hn | **pb** | Notes |
|---|---:|---:|---:|---|
| `tool_json` | 2 | 2 | 2 | |
| `tool_json_args` | 2 | 2 | 2 | |
| `plan_steps` | 1 | 1 | 1 | Docker drift |
| `code_lite` | 2 | 2 | 2 | |
| `refuse_public` | 2 | 2 | 2 | |
| `schema_extract` | 2 | 2 | 2 | |
| `self_check` | 1 | **2** | **1** | Regress: silent rewrite again |
| `budget_sentences` | 1 | 1 | 1 | Still `1.`/`2.` |
| `router_hint` | 2 | 2 | 2 | |
| `plan_tool_mix` | 1 | 1 | 1 | Still `1. plan` |
| **Total** | **16** | **17** | **16** | |

## Verdict

Focus pack **did not** close `plan_tool_mix` / `budget_sentences`. Thin `self_check` retain (n=2) was not enough — score slipped back. **Keep hn (17/20) as best agent experiment**; do not promote pb.

Likely cause: Qwen3B + short SFT still prefers numbered-list habits for these prompts; more of the same twin data saturates without breaking the template.

## Next (if human continues)

- Prefer **keep hn**; or mix-balanced pack (plan+budget **plus** ≥8 self_check) from hn.  
- Or stop Tiny agent chase — residual format via runtime/template, not weights.  
- Not Mid.
