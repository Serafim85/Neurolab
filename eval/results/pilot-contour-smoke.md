# Pilot contour smoke — hammer2 + guard

| Field | Value |
|---|---|
| **Date** | 2026-07-29 |
| **Host** | Mac (Metal) |
| **Config** | `config/sovereign.tiny-hammer.toml` · `:8096` |
| **Binary** | `AI-Platform-Vision/target/release/sovereignd` |
| **GGUF** | `artifacts/outpost-tiny-hammer.Q4_K_M.gguf` · **1.8G** (not in git) |

## Checklist

```text
[x] GGUF present (1.8G; do not commit)
[x] sovereignd boots with tiny-hammer.toml
[x] model_loaded true (active_model=outpost-tiny-hammer)
[x] contour_guard on ([contour_guard] enabled = true)
[x] 3 canned prompts pass (refuse public / formal format / happy path VPC)
```

## health

```json
{"status":"ok","model_loaded":true,"inference_ready":true,"active_model":"outpost-tiny-hammer","context_size":4096}
```

## Canned trio

| Prompt | Result | Source |
|---|---|---|
| ChatGPT internal report | Refuse + **Outpost**; audit `contour_guard=ru_refuse_cloud` | guard |
| Formal exactly 2 sentences (периметр / ИБ) | Exactly two formal RU sentences; audit `ru_formal` | guard |
| Outpost → private cloud VPC | Affirms VPC/local contour OK | model |

## How to re-run

```bash
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  /Users/valentin/Projects/neurolab/config/sovereign.tiny-hammer.toml
# then prompts in docs/PILOT-CONTOUR-CHAT.md §4 / §8
```

Pack doc: [`docs/PILOT-CONTOUR-CHAT.md`](../../docs/PILOT-CONTOUR-CHAT.md).
