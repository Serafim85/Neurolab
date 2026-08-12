# Brief N — Refresh stale verification numbers after wave 2

**Track:** Листы всё ещё говорят «51 tests» / «CI нет» / «11»  
**Primary repo:** `/Users/valentin/Projects/neurolab`  
**Read first:** `STATUS.md` Summary (CI / 85) · `docs/CLAIMS.md` C-50 · `scripts/gate.sh`  
**Wave:** 3 · **model preference:** cheap  
**Owns:** `docs/CLOSED-SANDBOX-VERIFY.md`, `docs/DEMO-PACK-SANDBOX.md`, и **только** другие `docs/**` файлы, где `rg` находит устаревшие «51 passed» / «CI в репозитории нет» / «11 passed» **кроме** `CLAIMS.md`, `STATUS.md`, `INVESTOR-*`, `AGENT-BRIEFS/**`

---

## Do exactly

1. Найти устаревшие цифры:

```bash
rg -n '51 passed|CI в репозитории нет|CI в репозитории нет|11 passed|нет CI' docs/ --glob '!AGENT-BRIEFS/**' --glob '!CLAIMS.md'
```

2. Обновить на актуальные (после wave 2): sandbox unit **85** (`not integration`),
   gate `scripts/gate.sh` 6 steps, CI = `.github/workflows/`. Не выдумывать
   integration-цифры без прогона.
3. Исторические упоминания «было 51» в Session log / CLAIMS — **не трогать**
   (CLAIMS вне ownership; session log в STATUS вне ownership кроме если N не владеет STATUS — N не владеет STATUS).
4. Минимальный diff.

---

## Do not

- `STATUS.md`, `CLAIMS.md`, `DECISIONS.md`, `CARD.md`, sandbox code.
- GTM / investor wording.
- `git commit`.

---

## Verify

```bash
rg -n '51 passed|CI в репозитории нет' docs/ --glob '!AGENT-BRIEFS/**' --glob '!CLAIMS.md' --glob '!SESSIONS*'
# допустимы только явные «было 51 → 85» как история
python3 scripts/check_doc_links.py
```

---

## Result file

`docs/AGENT-BRIEFS/results/N.md` — список файлов и старое→новое.
