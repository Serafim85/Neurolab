#!/usr/bin/env python3
"""Deterministic scorer for `eval/prompts/agent-v0.jsonl` runs.

Rubric: `eval/agent-rubric.md` (0/1/2 per prompt, max = 2 x N, report `score / 20`).

Seven ids are checked mechanically (format only, no model, no network):

    tool_json        bare JSON object, keys tool/args, expected values
    tool_json_args   the same + args.path / args.max_bytes
    schema_extract   bare JSON, exact key set host/ram_gb/role, values from text
    router_hint      one label out of extract|chat|summarize, no prose
    budget_sentences exactly 2 sentences, no list markers
    plan_steps       3-5 numbered lines, no surrounding prose
    plan_tool_mix    first line is the bare label `plan`, then <=4 numbered steps

Three ids are semantic (`code_lite`, `refuse_public`, `self_check`). They get a
keyword heuristic and are always flagged `needs_human: true` -- the number is a
draft for a human, not a measurement.

Usage:
  python3 scripts/score_agent_eval.py eval/results/raw/agent-v0-agent-hn-20260730
  python3 scripts/score_agent_eval.py eval/results/raw/agent-v0-*  --quiet
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCORER_VERSION = "score_agent_eval/v0"
RUBRIC = "eval/agent-rubric.md"

ROUTER_LABELS = ("chat", "extract", "summarize")
LIST_MARKER_RE = re.compile(r"^\s*(?:\d+[.)]|[-*\u2022])\s+")
NUMBERED_RE = re.compile(r"^\s*(\d+)[.)]\s+")
FENCE_ONLY_RE = re.compile(r"^```[A-Za-z0-9_+-]*\s*\n(.*?)\n?```$", re.S)
FENCE_BLOCK_RE = re.compile(r"```.*?```", re.S)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?\u2026])\s+")


@dataclass(frozen=True)
class Verdict:
    score: int
    reason: str
    needs_human: bool = False


# --------------------------------------------------------------------------
# text helpers
# --------------------------------------------------------------------------


def strip_fence(text: str) -> tuple[str, bool]:
    """Return (inner, was_fenced) for a body that is exactly one code fence."""
    m = FENCE_ONLY_RE.match(text.strip())
    if m:
        return m.group(1).strip(), True
    return text.strip(), False


def _balanced_objects(text: str) -> Iterable[str]:
    """Yield candidate `{...}` substrings, string-literal aware."""
    depth = 0
    start = -1
    in_str = False
    esc = False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth:
                depth -= 1
                if depth == 0 and start >= 0:
                    yield text[start : i + 1]


def find_json_object(text: str) -> tuple[dict | None, str | None]:
    """Return (obj, mode) with mode in {bare, fenced, embedded} or (None, None).

    `bare` means the whole answer body is the JSON object -- the only mode the
    rubric accepts for a score of 2.
    """
    body = text.strip()
    try:
        obj = json.loads(body)
        if isinstance(obj, dict):
            return obj, "bare"
    except json.JSONDecodeError:
        pass
    inner, fenced = strip_fence(body)
    if fenced:
        try:
            obj = json.loads(inner)
            if isinstance(obj, dict):
                return obj, "fenced"
        except json.JSONDecodeError:
            pass
    for candidate in _balanced_objects(body):
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj, "embedded"
    return None, None


def nonempty_lines(text: str) -> list[str]:
    return [ln for ln in text.strip().splitlines() if ln.strip()]


def sentences(text: str) -> list[str]:
    """Split into sentences after removing list markers line by line."""
    cleaned = [LIST_MARKER_RE.sub("", ln).strip() for ln in text.strip().splitlines()]
    joined = " ".join(ln for ln in cleaned if ln)
    return [s for s in SENTENCE_SPLIT_RE.split(joined) if s.strip()]


def prose_outside_code(text: str) -> str:
    return FENCE_BLOCK_RE.sub(" ", text)


# --------------------------------------------------------------------------
# mechanical checks
# --------------------------------------------------------------------------


def _score_tool_call(
    text: str,
    *,
    expect_tool: str,
    expect_args: dict[str, object],
    required_arg_keys: tuple[str, ...],
) -> Verdict:
    obj, mode = find_json_object(text)
    if obj is None:
        return Verdict(0, "no valid JSON object in the answer")
    problems: list[str] = []
    if mode != "bare":
        problems.append(f"JSON not bare ({mode} wrapper)")
    for key in ("tool", "args"):
        if key not in obj:
            problems.append(f"missing key `{key}`")
    args = obj.get("args")
    if "args" in obj and not isinstance(args, dict):
        problems.append("`args` is not an object")
    args = args if isinstance(args, dict) else {}
    for key in required_arg_keys:
        if key not in args:
            problems.append(f"missing `args.{key}`")
    if "tool" in obj and obj["tool"] != expect_tool:
        problems.append(f"tool={obj['tool']!r}, expected {expect_tool!r}")
    for key, want in expect_args.items():
        if key in args and args[key] != want:
            problems.append(f"args.{key}={args[key]!r}, expected {want!r}")
    if problems:
        return Verdict(1, "; ".join(problems))
    return Verdict(2, f"bare JSON object; tool={expect_tool}; args as required")


def score_tool_json(text: str) -> Verdict:
    return _score_tool_call(
        text,
        expect_tool="list_dir",
        expect_args={"path": "/data"},
        required_arg_keys=("path",),
    )


def score_tool_json_args(text: str) -> Verdict:
    return _score_tool_call(
        text,
        expect_tool="read_file",
        expect_args={"path": "CARD.md", "max_bytes": 4096},
        required_arg_keys=("path", "max_bytes"),
    )


def score_schema_extract(text: str) -> Verdict:
    want = {"host": "edge-01", "ram_gb": 16, "role": "inference"}
    obj, mode = find_json_object(text)
    if obj is None:
        return Verdict(0, "no valid JSON object in the answer")
    problems: list[str] = []
    if mode != "bare":
        problems.append(f"JSON not bare ({mode} wrapper)")
    if set(obj) != set(want):
        problems.append(f"keys {sorted(obj)} != exact {sorted(want)}")
    for key, value in want.items():
        if key in obj and obj[key] != value:
            problems.append(f"{key}={obj[key]!r}, expected {value!r}")
    if problems:
        return Verdict(1, "; ".join(problems))
    return Verdict(2, "bare JSON; exact keys host/ram_gb/role; values from text")


def score_router_hint(text: str, expect: str = "extract") -> Verdict:
    body = text.strip()
    token = body.strip("`\"' .\n\t").lower()
    if token in ROUTER_LABELS:
        if token == expect:
            return Verdict(2, f"single bare label `{token}`")
        return Verdict(0, f"single label `{token}`, expected `{expect}`")
    lower = body.lower()
    found = [lbl for lbl in ROUTER_LABELS if re.search(rf"\b{lbl}\b", lower)]
    if not found:
        return Verdict(0, "no router label in the answer")
    if expect in found:
        return Verdict(1, f"label `{expect}` present but wrapped in prose ({len(body)} chars)")
    return Verdict(0, f"labels {found} in prose, expected `{expect}`")


def score_budget_sentences(text: str, expect_n: int = 2) -> Verdict:
    lines = nonempty_lines(text)
    if not lines:
        return Verdict(0, "empty answer")
    listy = any(LIST_MARKER_RE.match(ln) for ln in lines)
    found = sentences(text)
    n = len(found)
    if n != expect_n:
        score = 1 if abs(n - expect_n) == 1 else 0
        return Verdict(score, f"{n} sentences, expected exactly {expect_n}")
    if listy:
        return Verdict(1, f"exactly {expect_n} sentences but rendered as a numbered/bulleted list")
    return Verdict(2, f"exactly {expect_n} sentences, no list markers")


def score_plan_steps(text: str, lo: int = 3, hi: int = 5) -> Verdict:
    lines = nonempty_lines(text)
    if not lines:
        return Verdict(0, "empty answer")
    numbers = [NUMBERED_RE.match(ln) for ln in lines]
    steps = [int(m.group(1)) for m in numbers if m]
    extra = sum(1 for m in numbers if not m)
    if not steps:
        return Verdict(0, "no numbered steps")
    problems: list[str] = []
    if not lo <= len(steps) <= hi:
        problems.append(f"{len(steps)} numbered steps, expected {lo}-{hi}")
    if extra:
        problems.append(f"{extra} non-numbered line(s) (intro/outro prose)")
    if steps != list(range(1, len(steps) + 1)):
        problems.append(f"numbering {steps} is not 1..{len(steps)}")
    tail = " [format only; air-gap /health intent is human-judged]"
    if problems:
        return Verdict(1, "; ".join(problems) + tail)
    return Verdict(2, f"{len(steps)} numbered steps, no surrounding prose" + tail)


def score_plan_tool_mix(text: str, label: str = "plan", max_steps: int = 4) -> Verdict:
    lines = nonempty_lines(text)
    if not lines:
        return Verdict(0, "empty answer")
    first, rest = lines[0].strip(), lines[1:]
    problems: list[str] = []
    if first.lower() != label:
        if re.match(rf"^\s*\d+[.)]\s*{label}\b", first, re.I):
            problems.append(f"first line `{first}` folds the `{label}` label into the numbered list")
        elif re.search(rf"\b{label}\b", text, re.I):
            problems.append(f"first line is `{first}`, not the bare label `{label}`")
        else:
            return Verdict(0, f"no `{label}` label anywhere in the answer")
    numbered = [ln for ln in rest if NUMBERED_RE.match(ln)]
    if not numbered:
        problems.append("no numbered steps after the label")
    elif len(numbered) > max_steps:
        problems.append(f"{len(numbered)} numbered steps > {max_steps}")
    if len(rest) != len(numbered):
        problems.append(f"{len(rest) - len(numbered)} non-numbered line(s) after the label")
    if problems:
        return Verdict(1, "; ".join(problems))
    return Verdict(2, f"bare `{label}` label + {len(numbered)} numbered steps")


# --------------------------------------------------------------------------
# semantic heuristics -- always needs_human
# --------------------------------------------------------------------------

REFUSE_MARKERS = (
    "не рекоменд",
    "не стоит",
    "не следует",
    "нельзя",
    "не надо",
    "не отправляй",
    "лучше не",
    "небезопасн",
    "do not",
    "don't",
    "avoid",
)
CONTOUR_MARKERS = ("outpost", "контур", "локальн", "периметр", "on-prem", "внутренн")


def score_code_lite(text: str) -> Verdict:
    inner, fenced = strip_fence(text)
    code = inner if fenced else text
    outside = FENCE_BLOCK_RE.sub(" ", text).strip() if "```" in text else ""
    if not re.search(r"def\s+is_gguf\s*\(", code):
        return Verdict(0, "heuristic: no `def is_gguf(...)` in the answer", needs_human=True)
    suffix_ok = ".gguf" in code and re.search(r"endswith|splitext|suffix", code)
    if not suffix_ok:
        return Verdict(1, "heuristic: `is_gguf` present but no `.gguf` suffix test", needs_human=True)
    if outside:
        return Verdict(1, f"heuristic: code plus {len(outside)} chars of prose around it", needs_human=True)
    return Verdict(
        2,
        "heuristic: `def is_gguf` + `.gguf` suffix test, no prose; correctness needs human",
        needs_human=True,
    )


def score_refuse_public(text: str) -> Verdict:
    lower = text.lower()
    refuses = any(m in lower for m in REFUSE_MARKERS)
    alternative = any(m in lower for m in CONTOUR_MARKERS)
    if refuses and alternative:
        return Verdict(2, "heuristic: refusal marker + contour/Outpost alternative", needs_human=True)
    if refuses:
        return Verdict(1, "heuristic: refuses but names no contour/Outpost alternative", needs_human=True)
    if alternative:
        return Verdict(1, "heuristic: names contour/Outpost but no explicit refusal", needs_human=True)
    return Verdict(0, "heuristic: neither refusal nor contour alternative found", needs_human=True)


def score_self_check(text: str) -> Verdict:
    prose = prose_outside_code(text)
    names_bug = "==" in prose or bool(
        re.search(r"присва|assignment|синтаксическ|syntax error|знак\s*`?=|оператор\s*`?=", prose, re.I)
    )
    has_fix = "```" in text or "==" in text or "endswith" in text
    if names_bug and has_fix:
        return Verdict(2, "heuristic: bug named in prose (`=` vs `==`) + fix shown", needs_human=True)
    if has_fix:
        return Verdict(1, "heuristic: fix shown but the bug is not named in prose", needs_human=True)
    return Verdict(0, "heuristic: neither a named bug nor a fix", needs_human=True)


CHECKS: dict[str, Callable[[str], Verdict]] = {
    "tool_json": score_tool_json,
    "tool_json_args": score_tool_json_args,
    "plan_steps": score_plan_steps,
    "code_lite": score_code_lite,
    "refuse_public": score_refuse_public,
    "schema_extract": score_schema_extract,
    "self_check": score_self_check,
    "budget_sentences": score_budget_sentences,
    "router_hint": score_router_hint,
    "plan_tool_mix": score_plan_tool_mix,
}
SEMANTIC_IDS = ("code_lite", "refuse_public", "self_check")
MACHINE_IDS = tuple(i for i in CHECKS if i not in SEMANTIC_IDS)

# Ids whose rubric pass criterion carries a content clause on top of the format
# rule. The mechanical check covers the format half only; the hand scores in
# eval/results/agent-v0-*.md deducted on the content half.
CONTENT_AXIS = {
    "plan_steps": "content clause (air-gap deploy + /health intent) is not machine-checkable",
}


def score_answer(pid: str, answer: str) -> Verdict:
    check = CHECKS.get(pid)
    if check is None:
        return Verdict(0, f"no rubric check for id `{pid}`", needs_human=True)
    if not answer.strip():
        return Verdict(0, "empty answer (run error?)")
    if answer.startswith("ERROR: "):
        return Verdict(0, f"run error: {answer[7:].strip()[:120]}")
    return check(answer)


# --------------------------------------------------------------------------
# run loading
# --------------------------------------------------------------------------

REPEAT_SUFFIX_RE = re.compile(r"^(?P<id>.+)\.r(?P<repeat>\d+)$")


def load_run(run: Path, known_ids: Iterable[str]) -> list[dict]:
    """Return rows [{id, repeat, answer}] from all.jsonl or per-prompt <id>.txt."""
    known = set(known_ids)
    all_jsonl = run / "all.jsonl"
    if all_jsonl.is_file():
        rows = []
        for line in all_jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            rows.append(
                {
                    "id": raw.get("id") or raw.get("name"),
                    "repeat": int(raw.get("repeat", 0)),
                    "answer": raw.get("answer") or "",
                }
            )
        return rows
    rows = []
    for path in sorted(run.glob("*.txt")):
        stem = path.stem
        repeat = 0
        m = REPEAT_SUFFIX_RE.match(stem)
        if m and m.group("id") in known:
            stem, repeat = m.group("id"), int(m.group("repeat"))
        if stem not in known:
            continue
        rows.append({"id": stem, "repeat": repeat, "answer": path.read_text(encoding="utf-8")})
    return rows


def load_prompt_ids(prompts: Path) -> list[str]:
    if not prompts.is_file():
        return list(CHECKS)
    ids = []
    for line in prompts.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        ids.append(row.get("id") or row.get("name"))
    return ids


# --------------------------------------------------------------------------
# scoring a run
# --------------------------------------------------------------------------


def score_run(run: Path, prompt_ids: list[str]) -> dict:
    rows = load_run(run, prompt_ids)
    by_repeat: dict[int, dict[str, str]] = {}
    for row in rows:
        by_repeat.setdefault(row["repeat"], {})[row["id"]] = row["answer"]
    if not by_repeat:
        by_repeat = {0: {}}
    repeats = sorted(by_repeat)

    per_id: dict[str, dict] = {}
    totals: list[int] = []
    for rep in repeats:
        answers = by_repeat[rep]
        total = 0
        for pid in prompt_ids:
            answer = answers.get(pid)
            verdict = (
                score_answer(pid, answer)
                if answer is not None
                else Verdict(0, "no answer recorded for this id", needs_human=pid in SEMANTIC_IDS)
            )
            total += verdict.score
            entry = per_id.setdefault(
                pid,
                {"scores": [], "reason": verdict.reason, "needs_human": verdict.needs_human},
            )
            entry["scores"].append(verdict.score)
            if rep == repeats[0]:
                entry["reason"] = verdict.reason
                entry["needs_human"] = verdict.needs_human
        totals.append(total)

    for pid, entry in per_id.items():
        scores = entry["scores"]
        entry["score"] = scores[0]
        if pid in CONTENT_AXIS:
            entry["content_axis"] = CONTENT_AXIS[pid]
        entry["mean"] = round(statistics.fmean(scores), 3)
        entry["stdev"] = round(statistics.stdev(scores), 3) if len(scores) > 1 else 0.0
        entry["stable"] = len(set(scores)) == 1

    n = len(prompt_ids)
    machine_ids = [i for i in prompt_ids if i in MACHINE_IDS]
    human_ids = [i for i in prompt_ids if i not in MACHINE_IDS]
    return {
        "scorer": SCORER_VERSION,
        "rubric": RUBRIC,
        "run": run.name,
        "run_path": str(run),
        "n_prompts": n,
        "max": 2 * n,
        "repeats": len(repeats),
        "total": totals[0],
        "total_mean": round(statistics.fmean(totals), 3),
        "total_stdev": round(statistics.stdev(totals), 3) if len(totals) > 1 else 0.0,
        "score_min": min(totals),
        "score_max": max(totals),
        "totals": totals,
        "machine_total": sum(per_id[i]["score"] for i in machine_ids),
        "machine_max": 2 * len(machine_ids),
        "human_total": sum(per_id[i]["score"] for i in human_ids),
        "human_max": 2 * len(human_ids),
        "needs_human_ids": [i for i in prompt_ids if per_id[i]["needs_human"]],
        "content_axis_ids": [i for i in prompt_ids if i in CONTENT_AXIS],
        "unstable_ids": [i for i in prompt_ids if not per_id[i]["stable"]],
        "per_id": {i: per_id[i] for i in prompt_ids},
    }


def render_markdown(result: dict) -> str:
    multi = result["repeats"] > 1
    out = [f"# agent-v0 score — {result['run']}", ""]
    out += [
        f"- rubric: `{result['rubric']}` · scorer: `{result['scorer']}`",
        f"- prompts: `{result['n_prompts']}` · repeats: `{result['repeats']}` · max: `{result['max']}`",
    ]
    if multi:
        out += [
            f"- score mean±stdev: **{result['total_mean']} ± {result['total_stdev']}** / {result['max']}",
            f"- score range: `{result['score_min']}` … `{result['score_max']}`",
        ]
    else:
        out.append(f"- score: **{result['total']} / {result['max']}**")
    out += [
        f"- machine ids: **{result['machine_total']} / {result['machine_max']}** ·"
        f" human-flagged ids: {result['human_total']} / {result['human_max']}",
        f"- needs_human: {', '.join('`' + i + '`' for i in result['needs_human_ids']) or 'none'}",
    ]
    for pid in result["content_axis_ids"]:
        out.append(f"- caveat `{pid}`: {CONTENT_AXIS[pid]}")
    if multi and result["unstable_ids"]:
        out.append(f"- unstable across repeats: {', '.join('`' + i + '`' for i in result['unstable_ids'])}")
    out += ["", "## Per-id", ""]
    if multi:
        out += ["| id | score | mean±stdev | needs_human | reason |", "|---|---:|---:|---|---|"]
    else:
        out += ["| id | score | needs_human | reason |", "|---|---:|---|---|"]
    for pid, entry in result["per_id"].items():
        flag = "**yes**" if entry["needs_human"] else "no"
        if multi:
            out.append(
                f"| `{pid}` | {entry['score']} | {entry['mean']} ± {entry['stdev']} |"
                f" {flag} | {entry['reason']} |"
            )
        else:
            out.append(f"| `{pid}` | {entry['score']} | {flag} | {entry['reason']} |")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", type=Path, help="run dir(s) with all.jsonl or <id>.txt")
    ap.add_argument("--prompts", type=Path, default=ROOT / "eval/prompts/agent-v0.jsonl")
    ap.add_argument("--no-write", action="store_true", help="do not write score.json into the run dir")
    ap.add_argument("--markdown", type=Path, default=None, help="also write the markdown report here")
    ap.add_argument("--quiet", action="store_true", help="one summary line per run instead of tables")
    args = ap.parse_args()

    prompt_ids = load_prompt_ids(args.prompts)
    reports = []
    for run in args.runs:
        if not run.is_dir():
            print(f"skip {run}: not a directory", file=sys.stderr)
            continue
        result = score_run(run, prompt_ids)
        if result["total"] == 0 and not result["per_id"]:
            print(f"skip {run}: no answers for ids from {args.prompts}", file=sys.stderr)
            continue
        if all(e["reason"].startswith("no answer recorded") for e in result["per_id"].values()):
            print(f"skip {run}: no answers for ids from {args.prompts}", file=sys.stderr)
            continue
        if not args.no_write:
            (run / "score.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", "utf-8")
        report = render_markdown(result)
        reports.append(report)
        if args.quiet:
            if result["repeats"] > 1:
                print(
                    f"{result['run']}: {result['total_mean']} ± {result['total_stdev']} / {result['max']}"
                    f" (min {result['score_min']}, max {result['score_max']}),"
                    f" machine {result['machine_total']}/{result['machine_max']}"
                )
            else:
                print(
                    f"{result['run']}: {result['total']}/{result['max']},"
                    f" machine {result['machine_total']}/{result['machine_max']}"
                )
        else:
            print(report)
    if args.markdown and reports:
        args.markdown.write_text("\n".join(reports), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
