# Datasets

| Path | Role |
|---|---|
| `manifest-tiny-lora-v0.md` | Tiny LoRA v0 passport (44) |
| `tiny-lora-v0/` | synthetic train JSONL + STATS |
| `manifest-tiny-lora-v1.md` | Tiny LoRA v1 passport (v0 + gap-fill) |
| `tiny-lora-v1/` | clarify / formal×2 / richer airgap |
| `base-qwen25-3b.md` | locked base GGUF pull notes |

Крупные чужие корпуса — только локально / USB; в git — manifests + наш синтетический seed.

```bash
python3 scripts/build_tiny_lora_data.py --version v1
```
