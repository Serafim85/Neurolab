# Brief K — result · hammer2 byte-alias

**Track:** Document hammer2 as alias of hammer (no GGUF delete)  
**Date:** 2026-08-13  
**Repo:** `/Users/valentin/Projects/neurolab`

## Files changed

| File | Change |
|---|---|
| `STATUS.md` | Ladder: alias note (SHA `3a712954…`); §Next item 7 → docs done, disk delete = human |
| `docs/CLAIMS.md` | C-01 caveat: two filenames, one byte artifact; do not cite as two models |
| `models/outpost-tiny/CARD.md` | Limits bullet: hammer2 is filename alias (manual block only) |

**Not done (forbidden):** GGUF delete, score changes, commit/push, DECISIONS/sandbox/CI.

## Verify

```bash
rg -n 'alias|byte-identical|3a712954' STATUS.md docs/CLAIMS.md models/outpost-tiny/CARD.md
python3 scripts/check_doc_links.py
python3 scripts/gen_model_card.py --check   # generated block untouched
```

## Session log line (for orchestrator)

- Brief K: `hammer2` GGUF documented as byte-alias of `hammer` (`3a712954…`); C-01 caveat; CARD Limits bullet; §Next #7 docs done — disk delete remains human (~1.8 GB).
