# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **Quality bar** | `outpost-tiny-v0` · **15/20** |
| **Latest GGUF name** | `outpost-tiny-v1` (content = **v1.2** train) · **12/20** |
| **Base** | Qwen2.5-3B-Instruct · Apache-2.0 |

## Eval ladder

| Version | Score | Note |
|---|---|---|
| Tiny-v0 | **15/20** | bar |
| Tiny-v1.1 | 14/20 | refuse broken |
| Tiny-v1.2 | 12/20 | refuse partial; fluency hit |

Sheets: `eval/results/tiny-v0-vs-baseline.md` · `tiny-v1.1-…` · `tiny-v1.2-…`

## Data

| Set | n | Role |
|---|---|---|
| `tiny-lora-v0` | 44 | seed |
| `tiny-lora-v1` | 74 | clarify/airgap |
| `tiny-lora-v1.2` | **92** | + hard ChatGPT refuse |

## Smoke

```bash
sovereignd config/sovereign.tiny-v0.toml   # :8091 quality bar
sovereignd config/sovereign.tiny-v1.toml   # :8092 experiment (latest v1.x GGUF)
```
