"""CLI: closed-sandbox run | diff | ask | stress | ui."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

from closed_sandbox.contour_ask import AskError, ask
from closed_sandbox.engine import EngineError, run_project
from closed_sandbox.manifest import ManifestError, load_project
from closed_sandbox.report import (
    diff_metrics,
    load_metrics_json,
    write_json,
    write_markdown,
)


def _cmd_run(args: argparse.Namespace) -> int:
    project = load_project(args.project)
    seed = args.seed
    metrics = run_project(project, seed=seed)
    out_dir = Path(args.out) if args.out else Path(project["_project_dir"]) / "out"
    write_json(metrics, out_dir / "metrics.json")
    write_markdown(metrics, out_dir / "report.md")
    if isinstance(metrics.get("chip_export"), dict):
        write_json(metrics["chip_export"], out_dir / "chip_export.json")
        print(f"wrote {out_dir / 'chip_export.json'}", file=sys.stderr)
    print(json.dumps(metrics, indent=2, sort_keys=True))
    print(f"wrote {out_dir / 'metrics.json'}", file=sys.stderr)
    print(f"wrote {out_dir / 'report.md'}", file=sys.stderr)
    return 0 if metrics.get("budget_ok") else 2


def _cmd_diff(args: argparse.Namespace) -> int:
    a = load_metrics_json(Path(args.a))
    b = load_metrics_json(Path(args.b))
    result = diff_metrics(a, b)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def _cmd_ask(args: argparse.Namespace) -> int:
    project = load_project(args.project)
    metrics_path = (
        Path(args.metrics)
        if args.metrics
        else Path(project["_project_dir"]) / "out" / "metrics.json"
    )
    if not metrics_path.is_file():
        raise AskError(
            f"metrics not found: {metrics_path}. Run `closed-sandbox run` first."
        )
    metrics = load_metrics_json(metrics_path)
    print(ask(project, metrics, args.question))
    return 0


def _cmd_stress(args: argparse.Namespace) -> int:
    """Sweep seeds; write summary JSON + markdown report."""
    project = load_project(args.project)
    seeds = list(range(args.seeds_from, args.seeds_from + args.n_seeds))
    out_dir = (
        Path(args.out) if args.out else Path(project["_project_dir"]) / "out" / "stress"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for seed in seeds:
        m = run_project(project, seed=seed)
        rows.append(m)
        write_json(m, out_dir / f"seed-{seed}.json")

    f1s = [float(r["f1"]) for r in rows]
    accs = [float(r["accuracy"]) for r in rows]
    spikes = [float(r["spike_count"]) for r in rows]
    walls = [float(r.get("wall_ms", 0.0)) for r in rows]
    budget_oks = sum(1 for r in rows if r.get("budget_ok"))

    summary = {
        "project_id": project["project"]["id"],
        "domain": project["project"]["domain"],
        "n_seeds": len(seeds),
        "seeds_from": args.seeds_from,
        "f1_mean": round(statistics.fmean(f1s), 4),
        "f1_stdev": round(statistics.pstdev(f1s), 4) if len(f1s) > 1 else 0.0,
        "f1_min": min(f1s),
        "f1_max": max(f1s),
        "accuracy_mean": round(statistics.fmean(accs), 4),
        "spike_count_mean": round(statistics.fmean(spikes), 1),
        "wall_ms_mean": round(statistics.fmean(walls), 1),
        "budget_ok_rate": round(budget_oks / len(rows), 4),
        "quality_per_kspike_mean": round(
            1000.0 * statistics.fmean(f1s) / max(statistics.fmean(spikes), 1.0), 6
        ),
        "worst_seed": seeds[f1s.index(min(f1s))],
        "best_seed": seeds[f1s.index(max(f1s))],
    }
    write_json(summary, out_dir / "summary.json")

    lines = [
        f"# Stress report — {summary['project_id']}",
        "",
        f"- domain: `{summary['domain']}`",
        f"- seeds: `{seeds[0]}…{seeds[-1]}` (n={summary['n_seeds']})",
        f"- f1 mean±stdev: **{summary['f1_mean']} ± {summary['f1_stdev']}**",
        f"- f1 range: `{summary['f1_min']}` … `{summary['f1_max']}`",
        f"- accuracy mean: `{summary['accuracy_mean']}`",
        f"- spike_count mean: `{summary['spike_count_mean']}`",
        f"- wall_ms mean: `{summary['wall_ms_mean']}`",
        f"- budget_ok rate: **{summary['budget_ok_rate']}**",
        f"- quality_per_kspike (mean f1): `{summary['quality_per_kspike_mean']}`",
        f"- worst seed: `{summary['worst_seed']}` · best: `{summary['best_seed']}`",
        "",
        "## Resource economy (v0)",
        "",
        "See `docs/NORTH-STAR-BUILD.md` §4 — quality under event cost.",
        "",
        "## Per-seed f1",
        "",
        "| seed | f1 | accuracy | spikes | budget_ok | wall_ms |",
        "|---|---:|---:|---:|---|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['seed']} | {r['f1']} | {r['accuracy']} | {r['spike_count']} | "
            f"{r['budget_ok']} | {r.get('wall_ms', '')} |"
        )
    lines.append("")
    (out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"wrote {out_dir / 'summary.json'}", file=sys.stderr)
    print(f"wrote {out_dir / 'report.md'}", file=sys.stderr)
    return 0 if summary["f1_mean"] >= args.min_mean_f1 else 3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="closed-sandbox")
    sub = p.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Run sandbox for a project.toml")
    run_p.add_argument("project", type=str, help="Path to project.toml")
    run_p.add_argument("--seed", type=int, default=None)
    run_p.add_argument("--out", type=str, default=None, help="Output directory")
    run_p.set_defaults(func=_cmd_run)

    diff_p = sub.add_parser("diff", help="Diff two metrics.json files")
    diff_p.add_argument("a", type=str)
    diff_p.add_argument("b", type=str)
    diff_p.set_defaults(func=_cmd_diff)

    ask_p = sub.add_parser("ask", help="Ask local/public LLM about metrics")
    ask_p.add_argument("project", type=str)
    ask_p.add_argument("question", type=str)
    ask_p.add_argument("--metrics", type=str, default=None)
    ask_p.set_defaults(func=_cmd_ask)

    stress_p = sub.add_parser("stress", help="Sweep seeds and write stress report")
    stress_p.add_argument("project", type=str)
    stress_p.add_argument("--n-seeds", type=int, default=20)
    stress_p.add_argument("--seeds-from", type=int, default=0)
    stress_p.add_argument("--out", type=str, default=None)
    stress_p.add_argument("--min-mean-f1", type=float, default=0.75)
    stress_p.set_defaults(func=_cmd_stress)

    ui_p = sub.add_parser(
        "ui", help="Serve CS-P03 Run + CS-P04 Diff + CS-P05 Ask local UI"
    )
    ui_p.add_argument("--host", type=str, default="127.0.0.1")
    ui_p.add_argument("--port", type=int, default=8765)
    ui_p.add_argument(
        "--open",
        action="store_true",
        help="Open default browser",
    )
    ui_p.set_defaults(func=_cmd_ui)

    return p


def _cmd_ui(args: argparse.Namespace) -> int:
    from closed_sandbox.ui_server import UiError, serve

    try:
        serve(host=args.host, port=args.port, open_browser=args.open)
    except UiError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int | None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        code = args.func(args)
    except (ManifestError, EngineError, AskError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    raise SystemExit(code)


if __name__ == "__main__":
    main()
