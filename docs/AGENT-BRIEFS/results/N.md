# Brief N — stale verify sheets refresh

**Track:** N · **Date:** 2026-08-13 · **Model:** cheap

## Files changed

| File | Old → New |
|---|---|
| `docs/CLOSED-SANDBOX-VERIFY.md` | Header «Last verified» без 85 → **85 passed (wave 2)** |
| `docs/CLOSED-SANDBOX-VERIFY.md` | §1 commands: только pytest → + `bash ../../scripts/gate.sh` |
| `docs/CLOSED-SANDBOX-VERIFY.md` | §1: нет CI → **CI:** `.github/workflows/ci.yml` (push/PR, 3.11+3.12) |
| `docs/CLOSED-SANDBOX-VERIFY.md` | §2 log: единственная актуальная строка **51 passed** → добавлена строка **85 passed**; 51 оставлен как wave 1 |
| `docs/CLOSED-SANDBOX-MVP.md` §9 | «unit **51 passed**» → «unit **85 passed** (было 51 до wave 2)» + gate/CI |
| `docs/DEMO-PACK-SANDBOX.md` | — (устаревших «51» / «CI нет» не найдено) |

## Verify

```bash
rg -n '51 passed|CI в репозитории нет' docs/ --glob '!AGENT-BRIEFS/**' --glob '!CLAIMS.md' --glob '!SESSIONS*'
# ожидаемо: 51 только как история в VERIFY §2 и MVP «было 51»
python3 scripts/check_doc_links.py
```

## Not touched (per brief)

- `STATUS.md`, `CLAIMS.md`, `DECISIONS.md`, `SESSIONS*`, `INVESTOR-*`, `AGENT-BRIEFS/**` (кроме этого result)
