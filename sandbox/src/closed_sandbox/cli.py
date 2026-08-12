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
    enrich_economy,
    load_metrics_json,
    write_json,
    write_markdown,
)

_STRESS_OPTIONAL_KEYS = (
    "f1",
    "accuracy",
    "spike_count",
    "synops",
    "latency_proxy_ms",
    "wall_ms",
    "chip_fit_score",
)
_STRESS_SKIP_COLS = frozenset(
    {
        "seed",
        "project_id",
        "domain",
        "by_scenario",
        "by_scenario_mode",
        "metric_primary",
        "economy_cost_key",
        "economy_cost_unit",
        "n_test",
    }
)


def _numeric_series(rows: list[dict], key: str) -> list[float]:
    vals: list[float] = []
    for row in rows:
        val = row.get(key)
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            vals.append(float(val))
    return vals


def _deprecated_min_mean_f1_action(option_strings: tuple[str, ...]) -> type[argparse.Action]:
    class _Action(argparse.Action):
        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: object,
            option_string: str | None = None,
        ) -> None:
            print(
                "warning: --min-mean-f1 is deprecated; use --min-primary",
                file=sys.stderr,
            )
            setattr(namespace, "min_primary", values)

    return _Action


def _stress_table_columns(rows: list[dict], primary: str) -> list[str]:
    present: set[str] = set()
    for row in rows:
        for key, val in row.items():
            if key in _STRESS_SKIP_COLS:
                continue
            if isinstance(val, (int, float, bool)):
                present.add(key)
    columns: list[str] = []
    seen: set[str] = set()
    if primary in present:
        columns.append(primary)
        seen.add(primary)
    for key in _STRESS_OPTIONAL_KEYS:
        if key in present and key not in seen:
            seen.add(key)
            columns.append(key)
    for key in sorted(present - seen - {"budget_ok"}):
        columns.append(key)
    if "budget_ok" in present:
        columns.append("budget_ok")
    return columns


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

    primary = str(rows[0].get("metric_primary", "f1"))
    primaries = _numeric_series(rows, primary)
    if not primaries:
        print(
            f"error: no numeric values for metric_primary={primary!r}",
            file=sys.stderr,
        )
        return 1

    walls = _numeric_series(rows, "wall_ms")
    budget_oks = sum(1 for r in rows if r.get("budget_ok"))

    summary: dict[str, object] = {
        "project_id": project["project"]["id"],
        "domain": project["project"]["domain"],
        "metric_primary": primary,
        "n_seeds": len(seeds),
        "seeds_from": args.seeds_from,
        f"{primary}_mean": round(statistics.fmean(primaries), 4),
        f"{primary}_stdev": round(statistics.pstdev(primaries), 4)
        if len(primaries) > 1
        else 0.0,
        f"{primary}_min": min(primaries),
        f"{primary}_max": max(primaries),
        "wall_ms_mean": round(statistics.fmean(walls), 1) if walls else 0.0,
        "budget_ok_rate": round(budget_oks / len(rows), 4),
        "worst_seed": seeds[primaries.index(min(primaries))],
        "best_seed": seeds[primaries.index(max(primaries))],
    }
    for key in _STRESS_OPTIONAL_KEYS:
        if key == primary or not any(key in r for r in rows):
            continue
        vals = _numeric_series(rows, key)
        if vals:
            summary[f"{key}_mean"] = round(
                statistics.fmean(vals), 4 if key != "spike_count" else 1
            )
    enriched = enrich_economy({primary: summary[f"{primary}_mean"], **rows[0]})
    if "quality_per_kspike" in enriched:
        summary["quality_per_kspike_mean"] = enriched["quality_per_kspike"]
    if "quality_per_ksynop" in enriched:
        summary["quality_per_ksynop_mean"] = enriched["quality_per_ksynop"]
    write_json(summary, out_dir / "summary.json")

    primary_mean = summary[f"{primary}_mean"]
    primary_stdev = summary[f"{primary}_stdev"]
    lines = [
        f"# Stress report — {summary['project_id']}",
        "",
        f"- domain: `{summary['domain']}`",
        f"- seeds: `{seeds[0]}…{seeds[-1]}` (n={summary['n_seeds']})",
        f"- primary (`{primary}`) mean±stdev: **{primary_mean} ± {primary_stdev}**",
        f"- primary range: `{summary[f'{primary}_min']}` … `{summary[f'{primary}_max']}`",
    ]
    for key in _STRESS_OPTIONAL_KEYS:
        mean_key = f"{key}_mean"
        if mean_key in summary:
            lines.append(f"- {key} mean: `{summary[mean_key]}`")
    lines.extend(
        [
            f"- wall_ms mean: `{summary['wall_ms_mean']}`",
            f"- budget_ok rate: **{summary['budget_ok_rate']}**",
        ]
    )
    if "quality_per_kspike_mean" in summary:
        lines.append(
            f"- quality_per_kspike: `{summary['quality_per_kspike_mean']}`"
        )
    if "quality_per_ksynop_mean" in summary:
        lines.append(
            f"- quality_per_ksynop: `{summary['quality_per_ksynop_mean']}`"
        )
    lines.extend(
        [
            f"- worst seed: `{summary['worst_seed']}` · best: `{summary['best_seed']}`",
            "",
            "## Resource economy (v0)",
            "",
            "See `docs/NORTH-STAR-BUILD.md` §4 — quality under event cost.",
            "",
            f"## Per-seed {primary}",
            "",
        ]
    )
    table_cols = _stress_table_columns(rows, primary)
    lines.append("| seed | " + " | ".join(table_cols) + " |")
    lines.append("|---|" + "|".join(["---:"] * len(table_cols)) + "|")
    for row in rows:
        cells = " | ".join(str(row.get(col, "")) for col in table_cols)
        lines.append(f"| {row['seed']} | {cells} |")
    lines.append("")
    (out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"wrote {out_dir / 'summary.json'}", file=sys.stderr)
    print(f"wrote {out_dir / 'report.md'}", file=sys.stderr)
    return 0 if float(summary[f"{primary}_mean"]) >= args.min_primary else 3


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
    stress_p.add_argument("--min-primary", type=float, default=0.75, dest="min_primary")
    stress_p.add_argument(
        "--min-mean-f1",
        type=float,
        action=_deprecated_min_mean_f1_action(("--min-mean-f1",)),
        help="deprecated alias for --min-primary",
    )
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
