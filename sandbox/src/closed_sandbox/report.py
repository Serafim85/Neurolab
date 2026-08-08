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

# Summary bullets printed only when the domain reported them (no `n/a` filler).
_HEADER_OPTIONAL_KEYS = (
    "f1",
    "accuracy",
    "spike_count",
    "synops",
    "latency_proxy_ms",
    "wall_ms",
)
_HEADER_LABELS = {
    "spike_count": "spike_count (avg)",
    "synops": "synops (avg)",
}

# Stable left-to-right order for `## Per scenario`; unknown keys sort after.
_SCENARIO_COLUMN_ORDER = (
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
    # Primary metric and the declared cost key must never be missing from a row.
    for key in (metrics.get("metric_primary"), metrics.get("economy_cost_key")):
        if (
            isinstance(key, str)
            and key not in row
            and isinstance(metrics.get(key), (int, float, bool))
        ):
            row[key] = metrics[key]

    metrics["by_scenario"] = {name: dict(row) for name in names}
    metrics["by_scenario_mode"] = "stub"
    return metrics


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def enrich_economy(metrics: dict[str, Any]) -> dict[str, Any]:
    """Add north-star resource proxies (NL-ADR-019 / NORTH-STAR-BUILD §4). No invented joules.

    Spike/synop proxies stay for spiking domains; any domain can additionally
    declare `[economy] cost_key` in its manifest to get `quality_per_unit_cost`.
    """
    out = dict(metrics)
    primary = out.get("metric_primary", "f1")
    quality = _number(out.get(primary, out.get("f1", out.get("accuracy"))))
    if quality is None:
        return out

    # Formulas unchanged (NORTH-STAR-BUILD §4); a zero cost has no ratio, so a
    # non-spiking domain gets no spike proxy instead of a meaningless 1000*q.
    spikes = _number(out.get("spike_count"))
    if spikes is not None and spikes > 0.0:
        out["quality_per_kspike"] = round(1000.0 * quality / max(spikes, 1.0), 6)
    synops = _number(out.get("synops"))
    if synops is not None and synops > 0.0:
        out["quality_per_ksynop"] = round(1000.0 * quality / max(synops, 1.0), 6)

    cost_key = out.get("economy_cost_key")
    if isinstance(cost_key, str) and cost_key:
        cost = _number(out.get(cost_key))
        # Zero / negative cost has no meaningful ratio — leave the proxy out.
        if cost is not None and cost > 0.0:
            out["quality_per_unit_cost"] = round(quality / cost, 6)
    return out


def write_json(metrics: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(enrich_economy(metrics), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _header_lines(m: dict[str, Any], primary: str) -> list[str]:
    """Summary bullets: primary always, the rest only when the domain reported them."""
    lines = [
        f"- domain: `{m.get('domain', '')}`",
        f"- seed: `{m.get('seed', '')}`",
        f"- primary (`{primary}`): **{m.get(primary, m.get('f1', 'n/a'))}**",
    ]
    for key in _HEADER_OPTIONAL_KEYS:
        if key == primary or key not in m:
            continue
        lines.append(f"- {_HEADER_LABELS.get(key, key)}: `{m[key]}`")
    lines.append(f"- budget_ok: **{m.get('budget_ok', 'n/a')}**")
    return lines


def _economy_lines(m: dict[str, Any], primary: str) -> list[str]:
    """Only the proxies this domain actually has — no `n/a` filler."""
    lines: list[str] = []
    if "quality_per_kspike" in m:
        lines.append(f"- quality_per_kspike: `{m['quality_per_kspike']}`")
    if "quality_per_ksynop" in m:
        lines.append(f"- quality_per_ksynop: `{m['quality_per_ksynop']}`")
    if "quality_per_unit_cost" in m:
        cost_key = m.get("economy_cost_key", "cost")
        unit = m.get("economy_cost_unit")
        label = f"`{primary}` per `{cost_key}`" + (f" ({unit})" if unit else "")
        lines.append(
            f"- quality_per_unit_cost [{label}]: `{m['quality_per_unit_cost']}`"
        )
    if not lines:
        lines.append(
            "- no cost proxy for this domain — declare `[economy] cost_key` "
            "in the manifest to get `quality_per_unit_cost`"
        )
    lines.append(f"- budget_ok: **{m.get('budget_ok', 'n/a')}**")
    return lines


def _scenario_columns(by_scenario: dict[str, Any], lead: tuple[str, ...]) -> list[str]:
    """Union of the keys rows actually have: lead keys, house order, then the rest.

    `budget_ok` is pinned last so the verdict reads at the end of the row.
    """
    present: set[str] = set()
    for row in by_scenario.values():
        if isinstance(row, dict):
            present.update(k for k in row if k != "n")

    columns: list[str] = []
    seen: set[str] = {"budget_ok"}

    def add(keys: Any) -> None:
        for key in keys:
            if key in present and key not in seen:
                seen.add(key)
                columns.append(key)

    add(lead)
    add(_SCENARIO_COLUMN_ORDER)
    add(sorted(present - seen))
    if "budget_ok" in present:
        columns.append("budget_ok")
    return ["n", *columns]


def _scenario_lines(by_scenario: dict[str, Any], lead: tuple[str, ...]) -> list[str]:
    columns = _scenario_columns(by_scenario, lead)
    header = "| scenario | " + " | ".join(columns) + " |"
    sep = "|---|" + "|".join(["---:"] * len(columns)) + "|"
    lines = ["## Per scenario", "", header, sep]
    for name, row in by_scenario.items():
        if not isinstance(row, dict):
            continue
        cells = " | ".join(str(row.get(col, "n/a")) for col in columns)
        lines.append(f"| {name} | {cells} |")
    lines.append("")
    return lines


def write_markdown(metrics: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    m = enrich_economy(metrics)
    primary = str(m.get("metric_primary", "f1"))
    lines = [
        f"# Sandbox report — {m.get('project_id', 'unknown')}",
        "",
        *_header_lines(m, primary),
        "",
        "## Resource economy (v0)",
        "",
        "North star proxies — quality under event cost. Not bio-joules "
        "(see `docs/NORTH-STAR-BUILD.md` §4).",
        "",
        *_economy_lines(m, primary),
        "",
    ]
    by_scenario = m.get("by_scenario")
    if isinstance(by_scenario, dict) and by_scenario:
        cost_key = m.get("economy_cost_key")
        lead = (primary, cost_key) if isinstance(cost_key, str) else (primary,)
        lines.extend(_scenario_lines(by_scenario, lead))
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
