#!/usr/bin/env bash
# Smoke: start sovereignd (sandbox-ask) if needed, run closed-sandbox ask.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SANDBOX="$ROOT/sandbox"
COMMERCIAL="${COMMERCIAL:-$HOME/Projects/AI-Platform-Vision}"
CFG="$ROOT/config/sovereign.sandbox-ask.toml"
PORT=8098
BASE="http://127.0.0.1:$PORT"
SOV="$COMMERCIAL/target/release/sovereignd"
[[ -x "$SOV" ]] || SOV="$COMMERCIAL/target/debug/sovereignd"

STARTED=0
if ! curl -sf -m 2 "$BASE/health" >/dev/null; then
  echo "Starting $SOV $CFG"
  "$SOV" "$CFG" >/tmp/sandbox-ask-sovereignd.log 2>&1 &
  echo $! >/tmp/sandbox-ask-sovereignd.pid
  STARTED=1
  for i in $(seq 1 120); do
    if curl -sf -m 2 "$BASE/health" >/dev/null; then
      break
    fi
    sleep 1
  done
  curl -sf "$BASE/health" | head -c 200
  echo
fi

cd "$SANDBOX"
export PYTHONPATH=src
python -m closed_sandbox.cli run examples/anomaly_v0/project.toml --out examples/anomaly_v0/out
# temporarily point ask at :8098 via env overlay in python one-liner
python - <<'PY'
from pathlib import Path
from closed_sandbox.manifest import load_project
from closed_sandbox.report import load_metrics_json
from closed_sandbox.contour_ask import ask

p = load_project("examples/anomaly_v0/project.toml")
p["contour"]["base_url"] = "http://127.0.0.1:8098/v1"
p["contour"]["provider"] = "local"
p["contour"]["model"] = "outpost-tiny-hammer"
m = load_metrics_json(Path("examples/anomaly_v0/out/metrics.json"))
print(ask(p, m, "State f1 and budget_ok from metrics. Under 60 words."))
PY

if [[ "$STARTED" -eq 1 ]]; then
  kill "$(cat /tmp/sandbox-ask-sovereignd.pid)" || true
fi
