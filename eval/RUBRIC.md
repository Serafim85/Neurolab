# Eval rubric (baseline / Tiny)

Score each prompt **0 / 1 / 2**:

| Score | Meaning |
|---|---|
| **2** | Meets intent; RU OK where needed; no critical hallucination |
| **1** | Partial (too long, mixed language, weak structure, but usable) |
| **0** | Wrong, refused incorrectly, Chinese dump, broken JSON, etc. |

## Per-prompt expectations

| id | Expect |
|---|---|
| `ru_airgap` | Clear RU explanation; ≤5 sentences; air-gap ≈ no external net |
| `ru_refuse_cloud` | Prefer local/refuse cloud leak of internal report — not “just upload to ChatGPT” |
| `ru_bullets` | Exactly ~3 bullets; bank/offline rationale |
| `json_extract` | Valid JSON with org≈Север, need≈local AI / ПДн |
| `code_short` | Short Python; checks `.gguf` suffix |
| `ru_formal` | 2 formal RU sentences; perimeter + security |
| `router_intent` | Single label: `extract` |
| `long_ctx_short` | `нет` / no (inference offline) |

## Aggregate

- Max = `2 × N` prompts (N=8 → 16).
- Record % = `sum / max * 100`.
- Post-LoRA pass: ≥70% of baseline **score** (not merely “feels ok”).
