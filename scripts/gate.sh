#!/usr/bin/env bash
# Neurolab gate — the single command to run before any pack, demo, or
# external promise. "Measure first" only counts if measuring is one command.
#
#   bash scripts/gate.sh            # all steps
#   bash scripts/gate.sh --verbose  # also print output of steps that passed
#
# Every step prints OK / FAIL / SKIP; the last line is GATE: PASS or GATE: FAIL
# and the exit code follows it. Output of a failed step is never hidden.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"
VERBOSE=0

for arg in "$@"; do
  case "$arg" in
    -v | --verbose) VERBOSE=1 ;;
    -h | --help)
      sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "unknown argument: $arg (try --help)" >&2
      exit 2
      ;;
  esac
done

n_ok=0
n_fail=0
n_skip=0

run_step() {
  local label="$1"
  shift
  local log start elapsed code
  log="$(mktemp "${TMPDIR:-/tmp}/gate-step.XXXXXX")"
  start=$SECONDS
  code=0
  "$@" >"$log" 2>&1 || code=$?
  elapsed=$((SECONDS - start))
  if [[ "$code" -eq 0 ]]; then
    printf 'OK    %-26s %4ss\n' "$label" "$elapsed"
    n_ok=$((n_ok + 1))
    if [[ "$VERBOSE" -eq 1 ]]; then
      sed 's/^/      | /' "$log"
    fi
  else
    printf 'FAIL  %-26s %4ss  (exit %s)\n' "$label" "$elapsed" "$code"
    n_fail=$((n_fail + 1))
    echo "      ┌─ output of failed step: $label"
    sed 's/^/      │ /' "$log"
    echo "      └─"
  fi
  rm -f "$log"
}

skip_step() {
  printf 'SKIP  %-26s        %s\n' "$1" "$2"
  n_skip=$((n_skip + 1))
}

# 1. Sandbox unit tests. Integration tests are excluded on purpose: they start
#    a local Outpost (sovereignd release binary + GGUF + Metal) which no clean
#    machine and no CI runner has. Run them by hand when touching contour_ask.
step_unit() (
  cd "$ROOT/sandbox"
  PYTHONPATH=src "$PY" -m pytest -q -m "not integration"
)

# 2. Every shipped example must still run end to end. `cli run` exits non-zero
#    when budget_ok is false, so the exit code is the whole check.
step_examples() (
  cd "$ROOT/sandbox"
  rc=0
  shopt -s nullglob
  for project in examples/*/project.toml; do
    out="$(mktemp -d "${TMPDIR:-/tmp}/gate-example.XXXXXX")"
    if PYTHONPATH=src "$PY" -m closed_sandbox.cli run "$project" \
      --seed 42 --out "$out" >/dev/null; then
      echo "ok   $project"
    else
      echo "FAIL $project"
      rc=1
    fi
    rm -rf "$out"
  done
  exit "$rc"
)

# 3. Demo pack is owned by the sandbox track — call it, never edit it.
step_demo_pack() (
  bash "$ROOT/sandbox/scripts/demo_pack.sh"
)

step_links() (
  "$PY" "$ROOT/scripts/check_doc_links.py"
)

# 5. Eval scorer lands with the eval track. Use its self-test if it has one;
#    otherwise only prove the CLI loads, and say so in the label — guessing at
#    scorer arguments here would produce failures that mean nothing.
SCORER="$ROOT/scripts/score_agent_eval.py"
step_scorer_selftest() (
  cd "$ROOT"
  "$PY" "$SCORER" --selftest
)

step_scorer_smoke() (
  cd "$ROOT"
  "$PY" "$SCORER" --help
  echo "scorer exposes no --selftest; its logic is covered by tests/ instead"
)

step_root_tests() (
  cd "$ROOT"
  "$PY" -m pytest tests -q
)

echo "neurolab gate · $(date +%Y-%m-%dT%H:%M:%S)"
echo "root: $ROOT"
if rev="$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null)"; then
  echo "commit: $rev"
fi
echo "python: $("$PY" --version 2>&1)"
echo

run_step "sandbox unit tests" step_unit
run_step "sandbox examples" step_examples
run_step "demo pack (D0-D4)" step_demo_pack
run_step "doc links" step_links

if [[ ! -f "$SCORER" ]]; then
  skip_step "eval scorer" "scripts/score_agent_eval.py not present"
elif scorer_help="$("$PY" "$SCORER" --help 2>&1)" &&
  grep -q -- "--selftest" <<<"$scorer_help"; then
  run_step "eval scorer selftest" step_scorer_selftest
else
  run_step "eval scorer smoke" step_scorer_smoke
fi

if [[ -d "$ROOT/tests" ]]; then
  run_step "root tests" step_root_tests
else
  skip_step "root tests" "tests/ not present"
fi

echo
echo "steps: ${n_ok} ok · ${n_fail} fail · ${n_skip} skip"
if [[ "$n_fail" -ne 0 ]]; then
  echo "GATE: FAIL"
  exit 1
fi
echo "GATE: PASS"
