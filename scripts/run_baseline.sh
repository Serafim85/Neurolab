#!/usr/bin/env bash
# Run eval/prompts.ru.jsonl against a local Outpost daemon.
# Prereq: sovereignd listening (default :8090).
#
# Optional:
#   BASE_URL=http://127.0.0.1:8091
#   GGUF=/path/to/active.gguf   # for meta SHA (defaults to base Qwen 3B)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMMERCIAL="${COMMERCIAL:-$HOME/Projects/AI-Platform-Vision}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8090}"
PROMPTS="$ROOT/eval/prompts.ru.jsonl"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT_DIR="$ROOT/eval/results/raw/baseline-$STAMP"
GGUF="${GGUF:-$ROOT/artifacts/base/Qwen2.5-3B-Instruct-Q4_K_M.gguf}"
MAX_TOKENS="${MAX_TOKENS:-256}"

mkdir -p "$OUT_DIR" "$ROOT/artifacts/base"

if ! curl -sf -m 2 "$BASE_URL/health" >/dev/null; then
  echo "No daemon at $BASE_URL/health"
  echo "Start (separate terminal):"
  SOV="$COMMERCIAL/target/release/sovereignd"
  if [[ ! -x "$SOV" ]]; then
    SOV="$COMMERCIAL/target/debug/sovereignd"
  fi
  echo "  $SOV $ROOT/config/sovereign.baseline.toml"
  echo "  # or: $SOV $ROOT/config/sovereign.tiny-v0.toml  → BASE_URL=http://127.0.0.1:8091"
  exit 1
fi

echo "Eval → $OUT_DIR (daemon $BASE_URL)"
{
  echo "gguf_path=$GGUF"
  if [[ -f "$GGUF" ]]; then
    echo "gguf=$(basename "$GGUF")"
    shasum -a 256 "$GGUF"
  else
    echo "gguf=MISSING (set GGUF= to active weights for SHA)"
  fi
} | tee "$OUT_DIR/meta.txt"
curl -sf "$BASE_URL/health" | tee "$OUT_DIR/health.json"
echo

while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue
  id="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["id"])' "$line")"
  prompt="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["prompt"])' "$line")"
  echo "=== $id ==="
  body="$(python3 -c '
import json,sys
prompt=sys.argv[1]
max_tokens=int(sys.argv[2])
print(json.dumps({
  "model": "default",
  "messages": [{"role":"user","content": prompt}],
  "max_tokens": max_tokens,
  "temperature": 0.2,
  "stream": False,
}))
' "$prompt" "$MAX_TOKENS")"
  resp="$(curl -sf -m 600 "$BASE_URL/v1/chat/completions" \
    -H 'Content-Type: application/json' \
    -d "$body")"
  echo "$resp" > "$OUT_DIR/$id.json"
  python3 -c '
import json,sys
p=json.load(open(sys.argv[1]))
print(p["choices"][0]["message"]["content"])
' "$OUT_DIR/$id.json" | tee "$OUT_DIR/$id.txt"
  echo
done < "$PROMPTS"

echo "Done. Score with eval/RUBRIC.md → eval/results/"
echo "Raw: $OUT_DIR"
echo "Tiny-v0 example:"
echo "  GGUF=$ROOT/artifacts/outpost-tiny-v0.Q4_K_M.gguf BASE_URL=http://127.0.0.1:8091 $0"
