# Train Outpost-Tiny LoRA → GGUF

> Data: `datasets/tiny-lora-v0/` · Scripts: `train_tiny_lora.py` · `merge_tiny_lora.py`  
> Canon: LoRA + Instruct post-train · Contour-safe (`CONTOUR-EGRESS.md`)

---

## 0. Stack choice

| Stack | Когда |
|---|---|
| **PEFT + TRL** (default) | Mac MPS / CUDA / CPU — наш скрипт |
| Unsloth | только NVIDIA CUDA / Colab — быстрее; тот же JSONL |

Не тащим Unsloth в default requirements (ломает Apple Silicon).

---

## 1. Setup

```bash
cd ~/Projects/neurolab
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-train.txt

# data (if missing)
python3 scripts/build_tiny_lora_data.py
```

HF скачает `Qwen/Qwen2.5-3B-Instruct` (~6 GB FP16). Нужен диск и сеть (lab machine).

---

## 2. Train

```bash
source .venv/bin/activate
python3 scripts/train_tiny_lora.py
# options:
#   --epochs 2 --lora-r 16 --device auto
#   --load-in-4bit   # CUDA QLoRA only
```

Артефакты:

```text
artifacts/runs/<stamp>/
  adapter/     # PEFT
  NOTES.md     # для Session log
  trainer/     # checkpoints HF trainer
```

**Mac M1:** ожидай медленный прогон (44 примера × 2 эпохи — терпимо).  
**CUDA 24 GB:** комфортно; можно `--batch-size 2 --load-in-4bit`.

---

## 3. Merge

```bash
python3 scripts/merge_tiny_lora.py \
  --adapter artifacts/runs/<stamp>/adapter \
  --out artifacts/hf/outpost-tiny-v0
```

---

## 4. Export GGUF

Нужен clone [llama.cpp](https://github.com/ggerganov/llama.cpp) (рядом или `LLAMA_CPP`).

```bash
export LLAMA_CPP="${LLAMA_CPP:-$HOME/Projects/llama.cpp}"
# convert (API скрипта может чуть отличаться по версии llama.cpp)
python3 "$LLAMA_CPP/convert_hf_to_gguf.py" \
  "$HOME/Projects/neurolab/artifacts/hf/outpost-tiny-v0" \
  --outfile "$HOME/Projects/neurolab/artifacts/outpost-tiny-v0.f16.gguf"

# quantize
"$LLAMA_CPP/llama-quantize" \
  "$HOME/Projects/neurolab/artifacts/outpost-tiny-v0.f16.gguf" \
  "$HOME/Projects/neurolab/artifacts/outpost-tiny-v0.Q4_K_M.gguf" \
  Q4_K_M

shasum -a 256 artifacts/outpost-tiny-v0.Q4_K_M.gguf \
  | tee artifacts/outpost-tiny-v0.Q4_K_M.SHA256.txt
```

Если `convert_hf_to_gguf.py` переименован — смотри README llama.cpp (`convert-hf-to-gguf.py`).

---

## 5. Smoke in Outpost

1. В `config/sovereign.baseline.toml` временно `path` → новый GGUF  
   **или** отдельный `config/sovereign.tiny-v0.toml`.
2. Запуск:

```bash
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  ~/Projects/neurolab/config/sovereign.baseline.toml
./scripts/run_baseline.sh
```

3. Score → `eval/results/tiny-v0-vs-baseline.md` (создать по RUBRIC).  
4. Обновить `models/outpost-tiny/CARD.md` provenance.

---

## 6. Unsloth (optional CUDA)

Тот же `train.messages.jsonl`. Псевдокод:

```python
from unsloth import FastLanguageModel
# load Qwen2.5-3B-Instruct 4bit, get_peft_model, SFTTrainer on messages
# save adapter → merge_tiny_lora.py as usual
```

Не дублируем полный Unsloth-скрипт, пока PEFT path не прогнан один раз.

---

## 7. Failure modes

| Симптом | Что делать |
|---|---|
| OOM на Mac | `--batch-size 1 --grad-accum 16 --max-seq-len 512` |
| Нет CUDA для 4bit | убрать `--load-in-4bit` |
| trl API error | `pip install -U trl transformers peft` |
| GGUF convert fail | сверить версию llama.cpp + Qwen arch support |

---

## 8. DoD

- [ ] `NOTES.md` в run dir
- [ ] merged HF + Q4 GGUF + SHA
- [ ] eval scored vs baseline
- [ ] CARD provenance filled
- [ ] STATUS Session log
