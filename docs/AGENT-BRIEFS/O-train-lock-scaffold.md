# Brief O — Dual requirements-train lock scaffold

**Track:** Лок с Apple Silicon не ставится на CUDA — два слота  
**Primary repo:** `/Users/valentin/Projects/neurolab`  
**Read first:** `docs/TRAIN-TINY-LORA.md` · `requirements-train.txt` · `docs/AGENT-BRIEFS/results/I.md` (про lock)  
**Wave:** 3 · **model preference:** cheap · **Slot:** 3  
**Owns:** `requirements-train.txt` (если нужна правка указателя), `docs/TRAIN-TINY-LORA.md` §1, новые placeholder-файлы lock **только если пустые маркеры**, не выдуманный freeze

---

## Do exactly

1. Описать в `TRAIN-TINY-LORA.md` два артефакта:
   - `requirements-train.macos-arm64.lock`
   - `requirements-train.cuda.lock`
2. Как снимать на каждой машине (`pip freeze` после install из `requirements-train.txt`).
3. **Не** генерировать полный lock с чужой платформы — либо пустой файл с
   `# generate on <platform>:` заголовком, либо только документация.
4. Упомянуть: лок ≠ лицензия весов; base всё ещё `qwen-research` на 3B.

---

## Do not

- Менять train scripts API.
- `git commit`.
- Скачивать CUDA-пакеты на Mac «для галочки».

---

## Result file

`docs/AGENT-BRIEFS/results/O.md`
