# Scripts

| Script | Role |
|---|---|
| `pull_base.sh` | download locked Tiny base GGUF |
| `run_baseline.sh` | eval prompts against Outpost :8090 |
| `build_tiny_lora_data.py` | regenerate `datasets/tiny-lora-v0/train.messages.jsonl` |
| `train_tiny_lora.py` | PEFT+TRL LoRA train → `artifacts/runs/<stamp>/adapter` |
| `merge_tiny_lora.py` | merge adapter → HF dir for GGUF convert |

Full recipe: [`docs/TRAIN-TINY-LORA.md`](../docs/TRAIN-TINY-LORA.md)
