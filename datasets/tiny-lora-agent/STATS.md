# tiny-lora-agent — mixed pack (30d)

Goal: lift `plan_tool_mix` + `budget_sentences` **without** regressing `self_check` (hn 17/20).

Total **49** · continue from `20260730-mps-agent-hn` · lr 1e-5 · f32 · 1 epoch

| tag | n |
|---|---:|
| `plan_label` | 15 |
| `budget_sentences` | 15 |
| `self_check` | 12 |
| `tool_json` | 2 |
| `router_label` | 1 |
| `schema_json` | 1 |
| `plan_steps` | 1 |
| `code_lite` | 1 |
| `refuse_public` | 1 |

**30a** 16 · **30b hn** **17** · **30c pb** 16 · **30d mix** **17** (plateau; keep hn/mix).

