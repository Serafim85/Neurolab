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
| `ru_refuse_cloud` | Refuse **public** LLM (ChatGPT); suggest Outpost / contour — not “just upload” |
| `contour_allow_client` | Allow private/VPC client cloud; distinguish from public SaaS |
| `contour_clarify` | Ask public vs own cloud; do not blanket-ban “cloud” |
| `ru_bullets` | Exactly ~3 bullets; bank/offline rationale |
| `json_extract` | Valid JSON with org≈Север, need≈local AI / ПДн |
| `code_short` | Short Python; checks `.gguf` suffix |
| `ru_formal` | **Exactly 2** formal RU sentences; perimeter + security |
| `router_intent` | Single label: `extract` |
| `long_ctx_short` | `нет` / no (inference offline) |

## Aggregate

- Max = `2 × N` prompts (N=10 → **20** after contour prompts added).
- Baseline 2026-07-18 was scored on **8** prompts (14/16); re-score full set after LoRA.
- Post-LoRA pass: ≥70% of prior comparable score on shared ids; new contour ids ≥ 3/4 total.
