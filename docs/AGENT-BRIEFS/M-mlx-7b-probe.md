# Brief M — MLX probe: can 7B LoRA fit M1 Pro 16 GB?

**Track:** Бесплатная проверка перед бюджетом GPU (NL-ADR-028)  
**Primary repo:** `/Users/valentin/Projects/neurolab`  
**Read first:** `docs/BASE-LICENSE.md` · `docs/DECISIONS.md` NL-ADR-028 · `docs/TRAIN-TINY-LORA.md` §0  
**Wave:** 3 · **model preference:** cheap · **Slot:** 2  
**Owns:** `docs/MLX-7B-PROBE.md` (новый) · optional one paragraph pointer in `docs/TRAIN-TINY-LORA.md` §0

---

## Do exactly

1. Выяснить по доке/командам (и по возможности dry-run на этой машине): ставится ли
   `mlx` / `mlx-lm`, есть ли Qwen2.5-7B-Instruct 4bit + LoRA путь.
2. Оценить **peak unified memory** для LoRA (не полный train ladder — probe).
3. Записать в `docs/MLX-7B-PROBE.md`:
   - go / no-go для обучения на M1 Pro 16 GB
   - точные команды install / dry-run
   - что блокирует (RAM, диск, API)
   - что это **не** меняет locked base (ADR-028 всё ещё Proposed)
4. Если полный download 7B невозможен — честный no-go с причиной, без выдуманных цифр.

---

## Do not

- Менять NL-ADR-002 / принимать ADR-028.
- Скачивать десятки GB без места (сейчас ~90 GB free — ок для одной 7B Q4 ~4–5 GB;
  FP16 ~15 GB тоже влезает, но не обязательно).
- `git commit`.
- Train всей лестницы.

---

## Verify

Файл существует; команды в нём копипастятся; нет утверждения «Apache на 3B».

---

## Result file

`docs/AGENT-BRIEFS/results/M.md` — go/no-go одной строкой сверху.
