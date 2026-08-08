#!/usr/bin/env bash
# Closed Sandbox demo pack — D0–D4 CLI smoke (fast path).
# Full 10-min show: see docs/DEMO-PACK-SANDBOX.md (UI + Gate optional).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:-}:src"

pass=0
fail=0

run_one() {
  local label="$1"
  local project="$2"
  local out
  out="$(mktemp -d "${TMPDIR:-/tmp}/cs-demo.XXXXXX")"
  echo "── $label"
  if ! PYTHONPATH=src python -m closed_sandbox.cli run "$project" --seed 42 --out "$out" >/dev/null 2>&1; then
    echo "FAIL  $label (cli exit)"
    fail=$((fail + 1))
    rm -rf "$out"
    return
  fi
  local ok domain
  ok="$(python3 -c "import json; d=json.load(open('$out/metrics.json')); print(d.get('budget_ok'))")"
  domain="$(python3 -c "import json; d=json.load(open('$out/metrics.json')); print(d.get('domain',''))")"
  if [[ "$ok" == "True" || "$ok" == "true" ]]; then
    echo "PASS  $label · domain=$domain · budget_ok=$ok"
    pass=$((pass + 1))
  else
    echo "FAIL  $label · domain=$domain · budget_ok=$ok"
    fail=$((fail + 1))
  fi
  rm -rf "$out"
}

echo "Closed Sandbox demo pack · domains D0–D4"
echo "cwd: $ROOT"
echo

run_one "D0 snn_lif"           "examples/anomaly_v0/project.toml"
run_one "D1 neuro_chip"        "examples/chip_estimate_v0/project.toml"
run_one "D1 fpga export"       "examples/chip_fpga_lite_v0/project.toml"
run_one "D2 biocompute"        "examples/biocompute_grn_v0/project.toml"
run_one "D3 biosignal"         "examples/biosignal_ecg_v0/project.toml"
run_one "D4 hybrid"            "examples/hybrid_ecg_snn_v0/project.toml"

echo
echo "result: ${pass} pass / ${fail} fail"
[[ "$fail" -eq 0 ]]

echo
echo "Next (manual, see docs/DEMO-PACK-SANDBOX.md):"
echo "  UI:   PYTHONPATH=src python -m closed_sandbox.cli ui"
echo "  Gate: Commercial sovereignd config/sovereign.synapse-gate.toml + ./scripts/synapse-gate-smoke.sh"
