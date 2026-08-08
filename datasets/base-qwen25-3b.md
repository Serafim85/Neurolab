# Base model — Qwen2.5-3B-Instruct Q4

**Locked for Outpost-Tiny v0 baseline.**

| | |
|---|---|
| Preset (Outpost CLI) | `qwen2.5-3b-instruct-q4` |
| Filename | `Qwen2.5-3B-Instruct-Q4_K_M.gguf` |
| Size | ~2.0 GB |
| License | **`qwen-research` — NON-COMMERCIAL only.** Не Apache-2.0. См. [`../docs/BASE-LICENSE.md`](../docs/BASE-LICENSE.md) |
| URL | https://huggingface.co/lmstudio-community/Qwen2.5-3B-Instruct-GGUF/resolve/main/Qwen2.5-3B-Instruct-Q4_K_M.gguf |

## Pull (recommended)

From Commercial repo (connected machine):

```bash
cd ~/Projects/AI-Platform-Vision
./target/release/sovereign model pull qwen2.5-3b-instruct-q4 \
  --dir ~/Projects/neurolab/artifacts/base
```

Or URL:

```bash
./target/release/sovereign model pull \
  --url "https://huggingface.co/lmstudio-community/Qwen2.5-3B-Instruct-GGUF/resolve/main/Qwen2.5-3B-Instruct-Q4_K_M.gguf" \
  --output ~/Projects/neurolab/artifacts/base/Qwen2.5-3B-Instruct-Q4_K_M.gguf
```

GGUF is gitignored. After download:

```bash
shasum -a 256 ~/Projects/neurolab/artifacts/base/Qwen2.5-3B-Instruct-Q4_K_M.gguf \
  | tee ~/Projects/neurolab/artifacts/base/SHA256.txt
```
