#!/usr/bin/env python3
"""Regenerate the machine-verifiable block of ``models/outpost-tiny/CARD.md``.

Every value in the generated block is read from disk or from the eval reports
at run time, so the passport cannot silently drift from the artifact it
describes. Hand-written sections of the card (purpose, limits, recipe) live
outside the markers and are never touched.

stdlib only, no network, idempotent apart from the generation date.

    python3 scripts/gen_model_card.py            # rewrite the block (hashes ~23 GB)
    python3 scripts/gen_model_card.py --skip-hash  # structure only, SHA = SKIPPED
    python3 scripts/gen_model_card.py --check    # exit 1 if the block is stale
    python3 scripts/gen_model_card.py --stdout   # print, do not write
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CARD = REPO / "models" / "outpost-tiny" / "CARD.md"

BEGIN = "<!-- BEGIN GENERATED: scripts/gen_model_card.py -->"
END = "<!-- END GENERATED: scripts/gen_model_card.py -->"

MISSING = "**MISSING**"
SKIPPED = "SKIPPED"

BASE_DIR = REPO / "artifacts" / "base"
BASE_NAME = "Qwen2.5-7B-Instruct"
BASE_ADR = "NL-ADR-028 (locked)"
BASE_GGUF_NAME = "Qwen2.5-7B-Instruct-Q4_K_M.gguf"

# Upstream license is a legal fact, not something this script may guess.
# It is reported MISSING until one of these lands in the repo.
LICENSE_CANDIDATES = (
    BASE_DIR / "LICENSE",
    BASE_DIR / "LICENSE.txt",
    BASE_DIR / "LICENSE.md",
    REPO / "docs" / "BASE-LICENSE.md",
)

# id -> GGUF file under artifacts/. Order is the order printed in the card.
ARTIFACTS = (
    ("7b-holes", "outpost-tiny-7b-holes.Q4_K_M.gguf"),
    ("7b-hammer (first 7B LoRA)", "outpost-tiny-7b-hammer.Q4_K_M.gguf"),
    ("hammer2 (pilot)", "outpost-tiny-hammer.Q4_K_M.gguf"),
    ("hammer2 (second copy)", "outpost-tiny-hammer2.Q4_K_M.gguf"),
    ("v0", "outpost-tiny-v0.Q4_K_M.gguf"),
    ("v0plus", "outpost-tiny-v0plus.Q4_K_M.gguf"),
    ("v1", "outpost-tiny-v1.Q4_K_M.gguf"),
    ("evalgold", "outpost-tiny-evalgold.Q4_K_M.gguf"),
    ("micro", "outpost-tiny-micro.Q4_K_M.gguf"),
    ("diverse", "outpost-tiny-diverse.Q4_K_M.gguf"),
    ("agent", "outpost-tiny-agent.Q4_K_M.gguf"),
    ("agent-hn", "outpost-tiny-agent-hn.Q4_K_M.gguf"),
    ("agent-pb", "outpost-tiny-agent-pb.Q4_K_M.gguf"),
    ("agent-mix", "outpost-tiny-agent-mix.Q4_K_M.gguf"),
)

# Model score and model+runtime score always stay separate rows. ``row`` is the
# substring identifying the line in the report that carries the number.
EVAL = (
    {
        "model": "7b-holes",
        "sheet": "prompts.ru.jsonl (N=10)",
        "setup": "GGUF alone, guard off",
        "report": "eval/results/tiny-7b-holes.md",
        "row": "| **7b-holes** |",
    },
    {
        "model": "7b-holes",
        "sheet": "prompts.ru.jsonl (N=10)",
        "setup": "+ Commercial `[contour_guard]` (ADR-047)",
        "report": "eval/results/tiny-7b-holes-plus-guard.md",
        "row": "| **Full** |",
        "split": True,
    },
    {
        "model": "7b-hammer",
        "sheet": "prompts.ru.jsonl (N=10)",
        "setup": "GGUF alone, guard off",
        "report": "eval/results/tiny-7b-hammer.md",
        "row": "| **7b-hammer** |",
    },
    {
        "model": "7b-hammer",
        "sheet": "prompts.ru.jsonl (N=10)",
        "setup": "+ Commercial `[contour_guard]` (ADR-047)",
        "report": "eval/results/tiny-7b-hammer-plus-guard.md",
        "row": "| **Full** |",
        "split": True,
    },
    {
        "model": "hammer2",
        "sheet": "prompts.ru.jsonl (N=10)",
        "setup": "GGUF alone, guard off",
        "report": "eval/results/tiny-hammer-ladder.md",
        "row": "| **hammer2** |",
    },
    {
        "model": "hammer2",
        "sheet": "prompts.ru.jsonl (N=10)",
        "setup": "+ Commercial `[contour_guard]` (ADR-047)",
        "report": "eval/results/tiny-hammer2-plus-guard.md",
        "row": "| **Full** |",
        "split": True,
    },
    {
        "model": "hammer2",
        "sheet": "prompts/agent-v0.jsonl (N=10)",
        "setup": "GGUF alone, guard off",
        "report": "eval/results/agent-v0-hammer2-baseline.md",
        "row": "| **Score** |",
    },
    {
        "model": "agent-hn",
        "sheet": "prompts/agent-v0.jsonl (N=10)",
        "setup": "GGUF alone, guard off",
        "report": "eval/results/agent-v0-agent-hn.md",
        "row": "| **Score** |",
    },
    {
        "model": "agent-hn",
        "sheet": "prompts/agent-v0.jsonl (N=10)",
        "setup": "+ Commercial `[agent_format]` v2, live",
        "report": "eval/results/agent-v0-runtime-format.md",
        "row": "| **Score** |",
        "split": True,
    },
)

SCORE_RE = re.compile(r"(\d{1,2})\s*/\s*20")
HEX64_RE = re.compile(r"\b([0-9a-f]{64})\b")
ROW_RE = re.compile(r"^\|\s*`?([A-Za-z_][\w]*)`?\s*\|\s*(\d)\s*\|\s*(.+?)\s*\|\s*$")
RAW_RE = re.compile(r"eval/results/raw/([\w.\-]+)")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sidecar_sha(gguf: Path) -> tuple[str | None, Path | None]:
    """Return the SHA recorded next to the artifact, if any."""
    stem = gguf.name[: -len(".gguf")] if gguf.name.endswith(".gguf") else gguf.stem
    for candidate in (
        gguf.parent / f"{stem}.SHA256.txt",
        gguf.parent / f"{gguf.name}.sha256",
        gguf.parent / f"{stem}.sha256",
    ):
        if candidate.is_file():
            found = HEX64_RE.search(candidate.read_text(encoding="utf-8", errors="replace"))
            if found:
                return found.group(1), candidate
    return None, None


def human_size(n: int) -> str:
    return f"{n / (1024 ** 3):.2f} GiB"


def read_report(rel: str) -> str | None:
    path = REPO / rel
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def parse_score(text: str, row: str) -> str:
    for line in text.splitlines():
        if row in line:
            found = SCORE_RE.search(line)
            if found:
                return f"{found.group(1)}/20"
            digits = re.findall(r"\*\*(\d{1,2})\*\*", line)
            if digits:
                return f"{digits[-1]}/20"
    return "UNPARSED"


def parse_source_split(text: str) -> str:
    """Count per-id score rows attributed to the model vs to runtime code."""
    model = runtime = 0
    for line in text.splitlines():
        found = ROW_RE.match(line)
        if not found:
            continue
        source = found.group(3).lower()
        if "guard" in source or "runtime" in source:
            runtime += 1
        elif "model" in source:
            model += 1
    total = model + runtime
    if total < 5:
        return "no per-id source column"
    return f"{model} model / {runtime} runtime (of {total})"


def parse_raw_evidence(text: str) -> str:
    names = RAW_RE.findall(text)
    if not names:
        return "**no raw dir referenced**"
    parts = []
    for name in dict.fromkeys(names):
        path = REPO / "eval" / "results" / "raw" / name
        if not path.is_dir():
            parts.append(f"`{name}` **absent**")
        elif not any(path.iterdir()):
            parts.append(f"`{name}` **empty**")
        else:
            parts.append(f"`{name}` {len(list(path.iterdir()))} files")
    return " · ".join(parts)


def base_block(skip_hash: bool) -> list[str]:
    preferred = BASE_DIR / BASE_GGUF_NAME
    # Incomplete curl of the 7B GGUF is a few hundred MB; real Q4 is ~4.5 GiB.
    ggufs = (
        [preferred]
        if preferred.is_file() and preferred.stat().st_size >= 1_000_000_000
        else []
    )
    lines = ["### Base", "", "| Field | Value |", "|---|---|"]
    lines.append(f"| Base model | {BASE_NAME} · {BASE_ADR} |")
    if not ggufs:
        lines.append(f"| Base GGUF | {MISSING} under `artifacts/base/` |")
        lines.append(f"| SHA256 (disk) | {MISSING} |")
    else:
        gguf = ggufs[0]
        digest = SKIPPED if skip_hash else sha256_file(gguf)
        lines.append(f"| Base GGUF | `{rel(gguf)}` · {human_size(gguf.stat().st_size)} |")
        lines.append(f"| SHA256 (disk) | `{digest}` |")
        recorded, where = sidecar_sha(gguf)
        if recorded is None:
            recorded_txt = BASE_DIR / "SHA256.txt"
            if recorded_txt.is_file():
                found = HEX64_RE.search(recorded_txt.read_text(encoding="utf-8"))
                recorded, where = (found.group(1) if found else None), recorded_txt
        if recorded is None:
            lines.append("| Recorded SHA | none on disk |")
        elif skip_hash:
            lines.append(f"| Recorded SHA | `{recorded}` (`{rel(where)}`) |")
        elif recorded == digest:
            lines.append(f"| Recorded SHA | match (`{rel(where)}`) |")
        else:
            lines.append(f"| Recorded SHA | **MISMATCH** `{recorded}` (`{rel(where)}`) |")
    found_license = next((p for p in LICENSE_CANDIDATES if p.is_file()), None)
    if found_license is None:
        lines.append(
            f"| Upstream LICENSE | {MISSING} — no license text recorded in this repo; "
            "required by `AGENTS.md` §5.7. Do not assume Apache-2.0 |"
        )
    else:
        lines.append(f"| Upstream LICENSE | `{rel(found_license)}` |")
    return lines


def artifacts_block(skip_hash: bool) -> tuple[list[str], dict[str, list[str]]]:
    lines = [
        "### Artifacts on disk",
        "",
        "| ID | GGUF | Size | SHA256 (disk) | Recorded SHA |",
        "|---|---|---|---|---|",
    ]
    by_digest: dict[str, list[str]] = {}
    for model_id, name in ARTIFACTS:
        path = REPO / "artifacts" / name
        if not path.is_file():
            lines.append(f"| {model_id} | `artifacts/{name}` | {MISSING} | {MISSING} | — |")
            continue
        size = path.stat().st_size
        digest = SKIPPED if skip_hash else sha256_file(path)
        recorded, where = sidecar_sha(path)
        if recorded is None:
            verdict = "**none on disk**"
        elif skip_hash:
            verdict = f"`{recorded[:12]}…`"
        elif recorded == digest:
            verdict = "match"
        else:
            verdict = f"**MISMATCH** `{recorded[:12]}…`"
        short = digest if skip_hash else f"`{digest[:16]}…{digest[-4:]}`"
        lines.append(
            f"| {model_id} | `artifacts/{name}` | {human_size(size)} | {short} | {verdict} |"
        )
        if not skip_hash:
            by_digest.setdefault(digest, []).append(name)
    return lines, by_digest


def duplicates_block(by_digest: dict[str, list[str]]) -> list[str]:
    dupes = {d: names for d, names in by_digest.items() if len(names) > 1}
    if not dupes:
        return []
    lines = ["### Byte-identical artifacts", ""]
    for digest, names in sorted(dupes.items()):
        joined = " · ".join(f"`{n}`" for n in sorted(names))
        lines.append(f"- `{digest[:16]}…` — {joined}")
    lines.append("")
    lines.append("Same bytes under different names: the file name does not identify a run.")
    return lines


def eval_block() -> list[str]:
    lines = [
        "### Eval — model and model+runtime are separate rows",
        "",
        "| Model | Sheet | Setup | Score | Per-id source | Report | Raw evidence |",
        "|---|---|---|---|---|---|---|",
    ]
    for entry in EVAL:
        text = read_report(entry["report"])
        if text is None:
            lines.append(
                f"| {entry['model']} | {entry['sheet']} | {entry['setup']} | {MISSING} "
                f"| — | `{entry['report']}` **absent** | — |"
            )
            continue
        score = parse_score(text, entry["row"])
        split = parse_source_split(text) if entry.get("split") else "not broken out"
        lines.append(
            f"| {entry['model']} | {entry['sheet']} | {entry['setup']} | **{score}** "
            f"| {split} | `{entry['report']}` | {parse_raw_evidence(text)} |"
        )
    lines += [
        "",
        "Scores are graded by hand (`eval/README.md`: no automatic scorer), single run,"
        " N=10, temp 0.2. A ±1 difference is not a measured improvement.",
        "Never merge a model row and a model+runtime row into one number."
        " Citable wording: [`docs/CLAIMS.md`](../../docs/CLAIMS.md).",
    ]
    return lines


def build_block(skip_hash: bool, today: str) -> str:
    art_lines, by_digest = artifacts_block(skip_hash)
    parts: list[str] = [
        BEGIN,
        "<!-- Generated by scripts/gen_model_card.py — do not edit by hand. -->",
        "",
        f"**Generated:** {today} · every value below is read from disk or from"
        " the named report at generation time.",
        "",
    ]
    parts += base_block(skip_hash)
    parts += ["", *art_lines]
    dupes = duplicates_block(by_digest)
    if dupes:
        parts += ["", *dupes]
    parts += ["", *eval_block(), "", END]
    return "\n".join(parts)


def splice(card_text: str, block: str) -> str:
    if BEGIN in card_text and END in card_text:
        head, rest = card_text.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
        return head + block + tail
    return card_text.rstrip("\n") + "\n\n" + block + "\n"


def strip_date(text: str) -> str:
    return re.sub(r"\*\*Generated:\*\* \d{4}-\d{2}-\d{2}", "**Generated:** <date>", text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--card", type=Path, default=CARD)
    parser.add_argument("--skip-hash", action="store_true", help="do not read GGUF bytes")
    parser.add_argument("--stdout", action="store_true", help="print the block, do not write")
    parser.add_argument("--check", action="store_true", help="exit 1 if the card is stale")
    args = parser.parse_args(argv)

    block = build_block(args.skip_hash, date.today().isoformat())

    if args.stdout:
        print(block)
        return 0

    if not args.card.is_file():
        print(f"card not found: {args.card}", file=sys.stderr)
        return 2

    current = args.card.read_text(encoding="utf-8")
    updated = splice(current, block)

    if args.check:
        if strip_date(current) == strip_date(updated):
            print(f"{rel(args.card)}: up to date")
            return 0
        print(f"{rel(args.card)}: STALE — rerun gen_model_card.py", file=sys.stderr)
        return 1

    if current == updated:
        print(f"{rel(args.card)}: unchanged")
        return 0
    args.card.write_text(updated, encoding="utf-8")
    print(f"{rel(args.card)}: written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
