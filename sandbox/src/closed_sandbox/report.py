"""Metrics report and version diff (domain-agnostic)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Scalars copied into stub by_scenario rows (engine ensure_*).
_SCENARIO_ROW_KEYS = (
    "f1",
    "accuracy",
    "spike_count",
    "synops",
    "latency_proxy_ms",
    "chip_fit_score",
    "budget_ok",
)


def ensure_by_scenario(
    metrics: dict[str, Any],
    project: dict[str, Any],
) -> dict[str, Any]:
    """Guarantee metrics.by_scenario for UI/report.

    Plugins that already set by_scenario (D0–D4 splits) are left unchanged.
    Fallback stub: one row per manifest scenario name from aggregate scalars
    (legacy / domains without a generative split).
    """
    existing = metrics.get("by_scenario")
    if isinstance(existing, dict) and existing:
        return metrics

    names = list(project.get("sandbox", {}).get("scenarios") or [])
    if not names:
        names = ["default"]

    row: dict[str, Any] = {
        "n": int(metrics["n_test"])
        if isinstance(metrics.get("n_test"), int)
        else 1,
    }
    for key in _SCENARIO_ROW_KEYS:
        val = metrics.get(key)
        if isinstance(val, (int, float, bool)):
            row[key] = val
    primary = metrics.get("metric_primary")
    if (
        isinstance(primary, str)
        and primary not in row
        and isinstance(metrics.get(primary), (int, float, bool))
    ):
        row[primary] = metrics[primary]

    metrics["by_scenario"] = {name: dict(row) for name in names}
    metrics["by_scenario_mode"] = "stub"
    return metrics


def enrich_economy(metrics: dict[str, Any]) -> dict[str, Any]:
    """Add north-star resource proxies (NL-ADR-019 / NORTH-STAR-BUILD §4). No invented joules."""
    out = dict(metrics)
    primary = out.get("metric_primary", "f1")
    quality = out.get(primary, out.get("f1", out.get("accuracy")))
    spikes = out.get("spike_count")
    if isinstance(quality, (int, float)) and isinstance(spikes, (int, float)):
        out["quality_per_kspike"] = round(1000.0 * float(quality) / max(float(spikes), 1.0), 6)
    synops = out.get("synops")
    if isinstance(quality, (int, float)) and isinstance(synops, (int, float)):
        out["quality_per_ksynop"] = round(1000.0 * float(quality) / max(float(synops), 1.0), 6)
    return out


def write_json(metrics: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(enrich_economy(metrics), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_markdown(metrics: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    m = enrich_economy(metrics)
    primary = m.get("metric_primary", "f1")
    lines = [
        f"# Sandbox report — {m.get('project_id', 'unknown')}",
        "",
        f"- domain: `{m.get('domain', '')}`",
        f"- seed: `{m.get('seed', '')}`",
        f"- primary (`{primary}`): **{m.get(primary, m.get('f1', 'n/a'))}**",
        f"- accuracy: `{m.get('accuracy', 'n/a')}`",
        f"- spike_count (avg): `{m.get('spike_count', 'n/a')}`",
        f"- synops (avg): `{m.get('synops', 'n/a')}`",
        f"- latency_proxy_ms: `{m.get('latency_proxy_ms', 'n/a')}`",
        f"- wall_ms: `{m.get('wall_ms', 'n/a')}`",
        f"- budget_ok: **{m.get('budget_ok', 'n/a')}**",
        "",
        "## Resource economy (v0)",
        "",
        "North star proxies — quality under event cost. Not bio-joules "
        "(see `docs/NORTH-STAR-BUILD.md` §4).",
        "",
        f"- quality_per_kspike: `{m.get('quality_per_kspike', 'n/a')}`",
        f"- quality_per_ksynop: `{m.get('quality_per_ksynop', 'n/a')}`",
        f"- budget_ok: **{m.get('budget_ok', 'n/a')}**",
        "",
    ]
    by_scenario = m.get("by_scenario")
    if isinstance(by_scenario, dict) and by_scenario:
        lines.extend(
            [
                "## Per scenario",
                "",
                "| scenario | n | f1 | accuracy | spike_count | synops |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for name, row in by_scenario.items():
            if not isinstance(row, dict):
                continue
            lines.append(
                "| {name} | {n} | {f1} | {acc} | {spikes} | {synops} |".format(
                    name=name,
                    n=row.get("n", "n/a"),
                    f1=row.get("f1", "n/a"),
                    acc=row.get("accuracy", "n/a"),
                    spikes=row.get("spike_count", "n/a"),
                    synops=row.get("synops", "n/a"),
                )
            )
        lines.append("")
    lines.extend(
        [
            "## Raw metrics",
            "",
            "```json",
            json.dumps(m, indent=2, sort_keys=True),
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def diff_metrics(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Compare two metrics dicts; numeric deltas where both sides are numbers."""
    keys = sorted(set(a) | set(b))
    changed: dict[str, Any] = {}
    for key in keys:
        if key.startswith("_"):
            continue
        va, vb = a.get(key), b.get(key)
        if va == vb:
            continue
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            changed[key] = {"a": va, "b": vb, "delta": vb - va}
        else:
            changed[key] = {"a": va, "b": vb}
    return {"changed": changed, "n_changed": len(changed)}


def load_metrics_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
