# Mid 14B as escalate brain — result

**Date:** 2026-07-29 · **NL-ADR-016**  
**Weights:** LM Studio `Qwen2.5-14B-Instruct-1M-Q4_K_M.gguf` (~8.4 GB) — already on disk  
**Config:** `config/sovereign.mid-escalate.toml` · `:8099`  
**Synapse evidence:** `benchmarks/results/2026-07-29-e5-outpost-brain-mid14.*`

## Found on machine

| Model | Path |
|---|---|
| 7B | `~/.lmstudio/.../Qwen2.5-7B-Instruct-1M-Q4_K_M.gguf` (+ `outpost/models/text/`) |
| **14B** | `~/.lmstudio/.../Qwen2.5-14B-Instruct-1M-Q4_K_M.gguf` |

## Bench (same E5 escalate set)

| Brain | Acc | Parse | Changed class | Wall |
|---|---|---|---|---|
| stub | 0.8561 | — | — | ~2 s |
| Tiny hammer2 (earlier) | 0.8561 | 18/18 | 0 | ~20 s |
| **Mid 14B** | **0.8561** | **18/18** | **0** | ~99 s |
| oracle | 0.8902 | — | — | ~2 s |

**Δ Mid − stub = 0.** Oracle gap still **+3.4 pp**.

## Read

- M1 16GB **can** load 14B Q4 (Metal ~8.5 GB) for lab escalate.  
- Bigger LLM on **the same top-k logits payload** still picks cascade argmax → no lift.  
- Lever is **not** Mid size for this task shape; need different brain job (features beyond logits, or accept escalate≠class fix).

## Do not

- Promote Mid to pilot chat (hammer2 20/20 stays).  
- Claim Mid closed oracle gap.

## Next levers (if still chase gap)

1. Escalate payload: calibrated full probs + uncertainty feats (not just top-5 logits).  
2. Separate specialist (not chat) on escalate rows.  
3. Live hit-rate into `mock` calib — honesty check only.
