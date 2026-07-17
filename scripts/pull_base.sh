#!/usr/bin/env bash
# Download locked Tiny base GGUF into artifacts/base/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMMERCIAL="${COMMERCIAL:-$HOME/Projects/AI-Platform-Vision}"
DEST_DIR="$ROOT/artifacts/base"
SOV="$COMMERCIAL/target/release/sovereign"
[[ -x "$SOV" ]] || SOV="$COMMERCIAL/target/debug/sovereign"

mkdir -p "$DEST_DIR"
echo "Using: $SOV"
"$SOV" model pull qwen2.5-3b-instruct-q4 --dir "$DEST_DIR"
shasum -a 256 "$DEST_DIR/Qwen2.5-3B-Instruct-Q4_K_M.gguf" | tee "$DEST_DIR/SHA256.txt"
echo "OK. Next: start sovereignd with config/sovereign.baseline.toml, then ./scripts/run_baseline.sh"
