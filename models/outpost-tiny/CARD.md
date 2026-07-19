# Outpost-Tiny — model card

| Field | Value |
|---|---|
| **Quality bar (use)** | `outpost-tiny-v0` · **15/20** · SHA `405b4443…ce27a7` |
| **Lab latest** | `outpost-tiny-v1` file = v1.2b train · **13/20** · SHA `273727a2…6f2d` |
| **Base** | Qwen2.5-3B-Instruct · Apache-2.0 |

**Quality bar** = GGUF we recommend for demo/pilot until a later train beats 15/20 on `eval/prompts.ru.jsonl`.

## Ladder

| Ver | Score |
|---|---|
| v0 | **15/20** |
| v1.1 | 14/20 |
| v1.2b (1ep) | 13/20 |
| v1.2 (2ep) | 12/20 |

## Smoke

```bash
# recommended
sovereignd config/sovereign.tiny-v0.toml   # :8091
```
