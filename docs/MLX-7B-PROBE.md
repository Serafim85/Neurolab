# MLX probe — Qwen2.5-7B-Instruct 4-bit LoRA on M1 Pro 16 GB

> **Date:** 2026-08-13 · **Machine:** Apple M1 Pro, 16 GB unified memory  
> **Verdict:** **GO** for MLX LoRA probe (peak **5.0 GB** measured)  
> **Does not change locked base** — NL-ADR-028 stays **Proposed**; 3B remains `qwen-research` (non-commercial), not Apache-2.0.

---

## 1. Verdict

| Question | Answer |
|---|---|
| `mlx` / `mlx-lm` install on this Mac? | Yes (`mlx` 0.32.0, `mlx-lm` 0.31.3) |
| Qwen2.5-7B-Instruct **4-bit + LoRA** path? | Yes — `mlx-community/Qwen2.5-7B-Instruct-4bit` + `mlx_lm lora` |
| Fits 16 GB unified memory? | **Yes** — mlx reported **Peak mem 5.022 GB** (1 iter, batch 1, seq 512, grad-checkpoint, 8 LoRA layers) |
| Default PEFT recipe (`train_tiny_lora.py`)? | **No** — `--load-in-4bit` is CUDA QLoRA only; Unsloth breaks Apple Silicon (`docs/TRAIN-TINY-LORA.md` §0) |

**GO** for a local MLX LoRA train on this box. **Not GO** as a drop-in replacement for the current PEFT script without a new merge/export step (§5).

---

## 2. Measured probe (2026-08-13)

```text
Model:     mlx-community/Qwen2.5-7B-Instruct-4bit  (~4.0 GB on disk)
Trainable: 0.076% (5.767M / 7615.617M params)
Iter 1:    Train loss 4.315 · Peak mem 5.022 GB · ~0.25 it/s
Adapter:   artifacts/mlx-probe/adapters/adapters.safetensors (~22 MB)
Exit:      0
```

Probe settings: `--batch-size 1 --max-seq-length 512 --num-layers 8 --grad-checkpoint --iters 1`.  
Log: `artifacts/mlx-probe/probe.log` (not committed — local only).

**Not measured:** full `max-seq-length 2048` or full tiny-lora dataset (44×2 epochs). Expect higher peak with longer seq / larger batch; 5 GB headroom on 16 GB still looks comfortable at batch 1.

---

## 3. Install (copy-paste)

```bash
cd ~/Projects/neurolab
python3 -m venv .venv-mlx-probe
source .venv-mlx-probe/bin/activate
pip install -U pip
pip install mlx mlx-lm
```

Optional: `export HF_TOKEN=…` — unauthenticated HF downloads are slow (~22 min for this model).

---

## 4. Dry-run (1 iteration, memory probe)

```bash
cd ~/Projects/neurolab
source .venv-mlx-probe/bin/activate

mkdir -p artifacts/mlx-probe/data artifacts/mlx-probe/adapters
head -2 datasets/tiny-lora-v0/train.messages.jsonl > artifacts/mlx-probe/data/train.jsonl
head -1 datasets/tiny-lora-v0/train.messages.jsonl > artifacts/mlx-probe/data/valid.jsonl

python -m mlx_lm lora \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --train \
  --data artifacts/mlx-probe/data \
  --adapter-path artifacts/mlx-probe/adapters \
  --iters 1 \
  --batch-size 1 \
  --max-seq-length 512 \
  --num-layers 8 \
  --grad-checkpoint \
  --steps-per-report 1 \
  --steps-per-eval 999 \
  --val-batches 1
```

Watch the line `Peak mem … GB` in output. Success saves `adapters/adapters.safetensors`.

---

## 5. Blockers / gaps

| Blocker | Detail |
|---|---|
| **Stack fork** | MLX path is separate from `scripts/train_tiny_lora.py` (PEFT+TRL). No `--load-in-4bit` on Mac MPS today. |
| **Export** | MLX adapter → merged HF → GGUF is not wired in lab scripts yet; needs human/ADR before product line. |
| **ADR-028** | Target 7B / licence escape is **Proposed only** — this probe does not accept NL-ADR-028 or supersede NL-ADR-002. |
| **Licence wording** | **3B** = `qwen-research`, non-commercial. **7B-Instruct** = Apache-2.0 (per `docs/BASE-LICENSE.md` / NL-ADR-028 context) — do not claim Apache on 3B. |
| **Disk** | Model cache ~4 GB; ~70 GB free after probe (was ~79 GB). OK for one 7B Q4; do not pull FP16 + Q4 + extras without plan. |
| **Network / HF** | First download ~4 GB; slow without `HF_TOKEN`. |
| **Seq length** | Probe used 512; production train may use 2048 — re-check peak before long runs. |

---

## 6. Fallback if MLX fails

Rented **CUDA ≥24 GB** + existing `train_tiny_lora.py --load-in-4bit` (QLoRA), or larger Mac — both need human budget (`NL-ADR-028` §Decision).

---

## 7. References

- NL-ADR-028 — `docs/DECISIONS.md` (Proposed)
- Licence facts — `docs/BASE-LICENSE.md`
- Default train recipe — `docs/TRAIN-TINY-LORA.md`
- MLX model — https://huggingface.co/mlx-community/Qwen2.5-7B-Instruct-4bit
