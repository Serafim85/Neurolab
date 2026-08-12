# Base model — Qwen2.5-7B-Instruct Q4

**Locked for Outpost-Tiny (NL-ADR-028, 2026-08-13).** Apache-2.0.

3B (`datasets/base-qwen25-3b.md`) is **research-only history**, not this lock.

| | |
|---|---|
| Filename | `Qwen2.5-7B-Instruct-Q4_K_M.gguf` |
| Size | ~4.7 GB |
| License | **Apache-2.0** (verified 2026-08-08: metadata + `LICENSE` body) |
| URL | https://huggingface.co/lmstudio-community/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf |
| LoRA train (Mac) | `mlx-community/Qwen2.5-7B-Instruct-4bit` via `scripts/train_mlx_lora.py` |

## Pull

```bash
curl -L --fail -o ~/Projects/neurolab/artifacts/base/Qwen2.5-7B-Instruct-Q4_K_M.gguf \
  "https://huggingface.co/lmstudio-community/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf"

shasum -a 256 ~/Projects/neurolab/artifacts/base/Qwen2.5-7B-Instruct-Q4_K_M.gguf \
  | tee -a ~/Projects/neurolab/artifacts/base/SHA256.txt
```

GGUF is gitignored. Record SHA in `artifacts/base/SHA256.txt` (both 3B archive and 7B lock).
