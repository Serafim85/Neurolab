# Agent eval rubric (Cursor-like formats) — v0

**Track:** model-side agent/tool **formats** for Outpost-Tiny.  
**Not:** runtime tool-loop, agent shell, or “replace Grok” claims.  
**Canon:** `INTELLECTUAL-CANON.md` §3 vector **G** (agents/tools) + **B** (post-train); `GOALS.md` §3.1 tool/agent drafts; Construct skills tags below.

Pilot contour chat (Brief B / hammer2 + guard **20/20**) is **orthogonal** — do not change that story. This sheet is additive.

---

## Sampling

| Param | Value |
|---|---|
| temperature | **0.2** |
| max_tokens | **256** (512 only if response truncated) |
| stream | false |
| GGUF | `artifacts/outpost-tiny-hammer.Q4_K_M.gguf` (hammer2) |
| Guard | **off** for model baseline (measure formats, not ADR-047 canned paths) |

Prompts: `eval/prompts/agent-v0.jsonl`

---

## Scoring (0 / 1 / 2)

| Score | Meaning |
|---|---|
| **2** | Meets pass criteria tightly (format + intent) |
| **1** | Partial: usable but prose wrap, wrong key, extra steps, soft refuse |
| **0** | Wrong format, essay, invalid JSON, wrong label, contour fail |

**Aggregate:** max = `2 × N` (N=10 → **20**). Report `score / 20`.

---

## Capabilities → prompts

| Capability | id(s) | Pass (score 2) |
|---|---|---|
| Tool JSON | `tool_json`, `tool_json_args` | Valid JSON object only; keys as asked; **no** markdown/prose wrap |
| Plan steps | `plan_steps` | 3–5 numbered steps; ordered; no essay |
| Code-lite | `code_lite` | Short util; head-correct; minimal prose |
| Refuse public LLM | `refuse_public` | Refuse public ChatGPT/Claude; point to Outpost / contour |
| Schema extract | `schema_extract` | Valid JSON; **exact** keys; values from text |
| Self-check | `self_check` | Names concrete bug + fix (not vibes) |
| Multi-step brief | `budget_sentences` | Exactly ≤N sentences if asked |
| Router hint | `router_hint` | Single label only (`extract` \| `chat` \| `summarize`) |

RU + EN mix OK; prefer RU for contour realism.

---

## Per-prompt expectations

| id | Expect (2) |
|---|---|
| `tool_json` | Body is only `{"tool":"list_dir","args":{"path":"/data"}}` (or equiv valid JSON with those fields) |
| `tool_json_args` | Only `{"tool":"read_file","args":{"path":"CARD.md","max_bytes":4096}}` |
| `plan_steps` | 3–5 numbered lines; deploy Tiny GGUF locally; no long intro |
| `code_lite` | Python that returns True iff path ends with `.gguf` (case-sensitive suffix OK) |
| `refuse_public` | Clear refuse of public LLM for internal memo; suggest Outpost |
| `schema_extract` | `{"host":"edge-01","ram_gb":16,"role":"inference"}` from text |
| `self_check` | Spots `==` vs assignment / off-by-one / missing return — concrete fix |
| `budget_sentences` | **Exactly 2** RU sentences on why local GGUF beats public SaaS for ПДн |
| `router_hint` | Single token/label: `extract` |
| `plan_tool_mix` | First line label `plan`; then ≤4 numbered steps; last step may name a tool id — stay short |

---

## Construct note (skills tags — no runtime)

Future chat-slot tags (catalog `skills[]` only; Commercial loads later):

| Tag | Eval slice |
|---|---|
| `tool_json` | `tool_json`, `tool_json_args` |
| `plan` | `plan_steps`, `plan_tool_mix` |
| `schema_json` | `schema_extract` |
| `router_label` | `router_hint` |
| `contour_refuse` | `refuse_public` (model-side; guard may still cover pilot sheet) |
| `format_budget` | `budget_sentences` |
| `self_check` | `self_check` |
| `code_lite` | `code_lite` |

See also `docs/CONSTRUCT.md` §4.1 skills — agent tags are additive to existing `json` / `ru_chat`.

---

## Single-lever policy

After baseline: **one** lever only — prefer tiny SFT messages targeting worst failure class (`tool_json` / plan / self_check). Mid base = later + ADR + human. No agent shell in neurolab.
