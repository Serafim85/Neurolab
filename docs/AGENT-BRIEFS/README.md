# Agent briefs — parallel tracks (2026-07-29)

> **Owner (human):** Valentin  
> **Orchestrator:** parent agent in neurolab  
> **Rule:** one brief = one agent = one primary repo. No cross-track STATUS wars.

## Tracks

| ID | Brief | Primary repo | Parallel? |
|---|---|---|---|
| **A** | [`A-closed-sandbox-studio.md`](A-closed-sandbox-studio.md) | `AI-Platform-Vision` | yes |
| **B** | [`B-contour-pilot-chat.md`](B-contour-pilot-chat.md) | `neurolab` | yes |
| **C** | [`C-cursor-like-agent-eval.md`](C-cursor-like-agent-eval.md) | `neurolab` | yes (docs/eval only; no GGUF train unless brief says) |
| **D** | [`D-brain-synapse-router.md`](D-brain-synapse-router.md) | `synapse` + neurolab docs | yes (docs only) |

## Shared rules (all agents)

1. Read your brief **fully** before editing.  
2. Read the linked SoT docs listed in the brief.  
3. Minimal diff. No drive-by refactors.  
4. **Do not commit** unless the brief or human says so.  
5. **Do not** write production web UI / React for Closed Sandbox.  
6. **Do not** commit `.gguf`, secrets, raw corpora.  
7. Write a short result file when done: `docs/AGENT-BRIEFS/results/<ID>.md` (in neurolab).  
8. Do **not** rewrite all of `STATUS.md` — only append your track’s Session log lines inside your result file; orchestrator merges STATUS.  
9. If blocked (missing binary, GPU, human ★), stop and report in `results/<ID>.md`.  
10. Russian or English OK in docs; keep IDs (`CS-L01`, `FR-UI-*`) stable.

## How to launch (Cursor)

Open four agent chats (or Task subagents). Paste:

```text
Execute brief at:
/Users/valentin/Projects/neurolab/docs/AGENT-BRIEFS/<FILE>.md
Follow every section. Write results/<LETTER>.md when done.
```

## Done when

Each `results/{A,B,C,D}.md` exists with: what changed, how to verify, blockers, next human step.
