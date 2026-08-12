# Brief K — Document hammer2 as byte-alias of hammer

**Track:** Убрать фантомную ступень лестницы без удаления GGUF с диска  
**Primary repo:** `/Users/valentin/Projects/neurolab`  
**Read first:** `docs/CLAIMS.md` C-01 · `STATUS.md` Ladder · `models/outpost-tiny/CARD.md` · `docs/BASE-LICENSE.md` (не менять)  
**Wave:** 3 · 2026-08-13 · **model preference:** cheap  
**Owns:** `STATUS.md` (только Ladder + одна Session-log строка в results), `models/outpost-tiny/CARD.md` (ручной блок caveats), `docs/CLAIMS.md` (строка C-01 / caveat про дубль)

---

## Факт (проверено 2026-08-08)

```text
SHA256 3a7129549bf19c69… = outpost-tiny-hammer.Q4_K_M.gguf
SHA256 3a7129549bf19c69… = outpost-tiny-hammer2.Q4_K_M.gguf
```

Остальные Q4 на диске — разные хеши. Удалять файл **не** надо (человек / 1.8 GB).

---

## Do exactly

1. **STATUS.md Ladder** — явно: hammer2 GGUF = alias of hammer (same SHA); score
   columns that differ are **eval/runtime history**, not two artifacts.
2. **CLAIMS.md** — усилить caveat у C-01 (или соседней internal-строки): два имени,
   один байтовый артефакт; не цитировать как две модели.
3. **CARD.md** (ручной блок, не ломая generated section) — одна bullet: hammer2
   is a filename alias; regenerating card with `gen_model_card.py` must still pass
   `--check` if you touch the machine block (prefer not to).
4. Не удалять `artifacts/outpost-tiny-hammer2.Q4_K_M.gguf`.
5. Не переписывать §Next целиком — максимум одна уточняющая строка, если пункт 7
   про дубль ещё висит: пометить «docs done; disk delete = human».

---

## Do not

- `DECISIONS.md`, sandbox, CI, LICENSE, investor docs.
- `git commit` / `push`.
- Менять числа 17/20 или 20/20 — только происхождение артефакта.

---

## Verify

```bash
# docs only
rg -n 'alias|byte-identical|3a712954' STATUS.md docs/CLAIMS.md models/outpost-tiny/CARD.md
python3 scripts/check_doc_links.py
# optional if CARD machine block untouched:
python3 scripts/gen_model_card.py --check
```

---

## Result file

`docs/AGENT-BRIEFS/results/K.md`
