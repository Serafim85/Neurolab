# GO — MLX 4-bit LoRA fits M1 Pro 16 GB (peak 5.0 GB measured)

**Track:** M · **Date:** 2026-08-13 · **Model:** cheap

## Files changed

| File | Change |
|---|---|
| `docs/MLX-7B-PROBE.md` | New — install/dry-run commands, measured peak mem, blockers |
| `docs/TRAIN-TINY-LORA.md` §0 | One-paragraph MLX pointer |

**Not done (forbidden):** NL-ADR-028 accept, NL-ADR-002 edit, train ladder, git commit/push.

## Verify

```bash
test -f docs/MLX-7B-PROBE.md
head -1 docs/AGENT-BRIEFS/results/M.md   # GO line
rg -n 'Apache.*3B|3B.*Apache' docs/MLX-7B-PROBE.md   # should be absent or negated
```

## Key numbers (measured, not invented)

- Peak mem: **5.022 GB** (`mlx_lm lora`, batch 1, seq 512, grad-checkpoint)
- Model cache: **~4.0 GB** (`mlx-community/Qwen2.5-7B-Instruct-4bit`)
- Disk free after probe: **~70 GB**
