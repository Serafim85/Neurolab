#!/usr/bin/env python3
"""Map Synapse E5 bench JSON → Closed Sandbox synapse_import fixture.

Supports:
  - legacy *-e5-brain-escalate.json (focus.local_acc)
  - brains-v2 *-e5-brains-v2-*.json (rows.specialist / stage_vote / …)

Usage:

  python sandbox/scripts/export_synapse_e5_fixture.py \\
    --bench ~/Projects/synapse/benchmarks/results/2026-08-01-e5-brains-v2-skip-llm.json \\
    --out sandbox/examples/synapse_e5_import/fixtures/e5-official.json
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def _newest_bench(results: Path) -> Path:
    cands = sorted(results.glob("*-e5-brains-v2*.json")) + sorted(
        results.glob("*-e5-brain-escalate.json")
    )
    if not cands:
        raise SystemExit(f"no E5 bench JSON under {results}")
    return sorted(cands, key=lambda p: p.stat().st_mtime)[-1]


def to_fixture(bench: dict, *, source_path: Path) -> dict:
    """Build synapse_import fixture; prefer specialist as class_fix (BRAIN-BRIDGE v0.3)."""
    if "rows" in bench and isinstance(bench["rows"], dict):
        rows = bench["rows"]
        stub = float((rows.get("stub") or {}).get("acc", 0.0))
        vote = float((rows.get("stage_vote") or {}).get("acc", 0.0))
        specialist = float((rows.get("specialist") or {}).get("acc", 0.0))
        rescue = (rows.get("rescue") or {}).get("acc")
        oracle = float((rows.get("oracle") or {}).get("acc", 0.0))
        esc = float((rows.get("specialist") or rows.get("stage_vote") or {}).get("escalate_rate", 0.0))
        bcr = float((rows.get("specialist") or rows.get("stage_vote") or {}).get("brain_call_rate", 0.0))
        wall = float((rows.get("specialist") or {}).get("wall_s", 0.0))
        n = int((rows.get("specialist") or {}).get("n", 0) or 0)
        lat_ms = (wall / n * 1000.0) if n else 0.0
        primary = specialist if specialist else vote
        class_fix = "specialist" if specialist else "stage_vote"
        notes = (
            f"Roles v0.3: class_fix={class_fix} "
            f"(+{(primary - stub) * 100:.2f} pp vs stub); "
            "Outpost=explain/plan only. spike/synops N/A host wrap. "
            "oracle_accuracy lab upper bound."
        )
        out = {
            "pack": "e5-brain-escalate",
            "adr": bench.get("adr", "SYN-ADR-008"),
            "source_lab": "synapse",
            "date": date.today().isoformat(),
            "accuracy": primary,
            "f1": primary,
            "stub_accuracy": stub,
            "stage_vote_accuracy": vote,
            "specialist_accuracy": specialist,
            "oracle_accuracy": oracle,
            "escalate_rate": esc,
            "brain_call_rate": bcr,
            "class_fix": class_fix,
            "brain_role": "explain_plan",
            "bridge_version": "0.3.0",
            "spike_count": 0,
            "synops": 0,
            "latency_proxy_ms": round(lat_ms, 2),
            "n_neurons": 0,
            "n_synapses": 0,
            "budget_ok": True,
            "mid_backend": bench.get("mid_backend"),
            "focus_policy": "hard_or_low_score",
            "portable_pass": True,
            "escalate_policy_ok": True,
            "bench_source": str(source_path),
            "notes": notes,
        }
        if rescue is not None:
            out["rescue_accuracy"] = float(rescue)
        return out

    # Legacy focus.* shape
    focus = bench.get("focus") or {}
    lat = (bench.get("latency_per_sample_ms") or {}).get("portable", 0.0)
    local_acc = float(focus.get("local_acc", 0.0))
    return {
        "pack": "e5-brain-escalate",
        "adr": bench.get("adr", "SYN-ADR-008"),
        "source_lab": "synapse",
        "date": date.today().isoformat(),
        "accuracy": local_acc,
        "f1": local_acc,
        "oracle_accuracy": float(focus.get("oracle_acc", 0.0)),
        "escalate_rate": float(focus.get("escalate_rate", 0.0)),
        "brain_call_rate": float(focus.get("brain_call_rate", 0.0)),
        "class_fix": "specialist",
        "brain_role": "explain_plan",
        "bridge_version": "0.3.0",
        "spike_count": 0,
        "synops": 0,
        "latency_proxy_ms": float(lat),
        "n_neurons": 0,
        "n_synapses": 0,
        "budget_ok": True,
        "mid_backend": bench.get("mid_backend"),
        "focus_policy": bench.get("focus_policy", "hard_or_low_score"),
        "portable_pass": bench.get("portable_pass"),
        "escalate_policy_ok": bench.get("escalate_policy_ok"),
        "bench_source": str(source_path),
        "notes": (
            "Live export from Synapse E5 bench. "
            "spike/synops N/A for host wrap — zeros. "
            "oracle_accuracy is lab upper bound, not product KPI."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--synapse-root",
        type=Path,
        default=Path.home() / "Projects" / "synapse",
    )
    ap.add_argument("--bench", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    results = args.synapse_root / "benchmarks" / "results"
    bench_path = args.bench or _newest_bench(results)
    if not bench_path.is_file():
        raise SystemExit(f"bench not found: {bench_path}")

    neurolab = Path(__file__).resolve().parents[2]
    out = args.out or (
        neurolab
        / "sandbox"
        / "examples"
        / "synapse_e5_import"
        / "fixtures"
        / "e5-official.json"
    )

    bench = json.loads(bench_path.read_text(encoding="utf-8"))
    fixture = to_fixture(bench, source_path=bench_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.is_file():
        bak = out.with_suffix(out.suffix + ".bak")
        bak.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"backup {bak}")
    out.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(fixture, indent=2))
    print(f"wrote {out}")
    print(f"from  {bench_path}")


if __name__ == "__main__":
    main()
