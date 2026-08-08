#!/usr/bin/env python3
"""Check relative markdown links point at existing files.

Stdlib only, so it runs on a clean CI runner and locally without install:

    python3 scripts/check_doc_links.py            # default doc set
    python3 scripts/check_doc_links.py docs/X.md  # explicit files/dirs

Anchors are NOT validated: for `FILE.md#section` only `FILE.md` is checked.
Validating anchors would need a heading parser per target file and would
turn every heading rename into a CI failure; the file part catches the
breakage that actually matters (moved/renamed docs).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# docs/** plus the three entry points a reader hits first.
DEFAULT_TARGETS = ("docs", "AGENTS.md", "STATUS.md", "README.md")

# Directories never scanned even if they contain markdown.
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "artifacts"}

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
# [text](target) and ![alt](target); target may carry a "title".
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]*)\)")
# [label]: target  — reference-style definition.
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")


class Link:
    __slots__ = ("source", "line", "raw", "target")

    def __init__(self, source: Path, line: int, raw: str, target: str) -> None:
        self.source = source
        self.line = line
        self.raw = raw
        self.target = target


def strip_code(text: str) -> list[str]:
    """Blank out fenced blocks and inline code, keeping line numbering."""
    lines = text.splitlines()
    out: list[str] = []
    fence: str | None = None
    for line in lines:
        match = FENCE_RE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0]
                out.append("")
                continue
            out.append(INLINE_CODE_RE.sub("", line))
        else:
            if match and match.group(1)[0] == fence:
                fence = None
            out.append("")
    return out


def clean_target(raw: str) -> str:
    """Strip <>, an optional link title, and percent-encoding."""
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        for quote in ('"', "'"):
            pos = target.find(f" {quote}")
            if pos != -1:
                target = target[:pos]
                break
        target = target.split()[0] if target.split() else ""
    return unquote(target.strip())


def is_external(target: str) -> bool:
    return (
        not target
        or target.startswith("#")
        or target.startswith("//")
        or target.startswith("~")
        or bool(SCHEME_RE.match(target))
    )


def collect_links(path: Path) -> list[Link]:
    text = path.read_text(encoding="utf-8", errors="replace")
    links: list[Link] = []
    for number, line in enumerate(strip_code(text), start=1):
        raws = INLINE_LINK_RE.findall(line)
        ref = REF_DEF_RE.match(line)
        if ref:
            raws = [*raws, ref.group(1)]
        for raw in raws:
            target = clean_target(raw)
            links.append(Link(path, number, raw.strip(), target))
    return links


def iter_markdown(root: Path, targets: list[str]) -> list[Path]:
    found: list[Path] = []
    for name in targets:
        path = (root / name) if not Path(name).is_absolute() else Path(name)
        if path.is_file():
            found.append(path)
        elif path.is_dir():
            for md in sorted(path.rglob("*.md")):
                if SKIP_DIRS.isdisjoint(md.parts):
                    found.append(md)
        else:
            print(f"warning: no such path: {path}", file=sys.stderr)
    return sorted(set(found))


def resolve(link: Link, root: Path) -> Path | None:
    """Return the resolved path, or None when the link is not checkable."""
    file_part = link.target.split("#", 1)[0]
    if not file_part:
        return None
    if file_part.startswith("/"):
        absolute = Path(file_part)
        # Either a real absolute path or a repo-root-relative one.
        return absolute if absolute.exists() else root / file_part.lstrip("/")
    return link.source.parent / file_part


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail if a relative markdown link points at a missing file."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help=f"files or dirs to scan (default: {' '.join(DEFAULT_TARGETS)})",
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="repository root (default: parent of scripts/)",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    files = iter_markdown(root, list(args.targets) or list(DEFAULT_TARGETS))

    checked = 0
    skipped = 0
    broken: list[tuple[Link, Path]] = []
    for path in files:
        for link in collect_links(path):
            if is_external(link.target):
                skipped += 1
                continue
            resolved = resolve(link, root)
            if resolved is None:
                skipped += 1
                continue
            checked += 1
            if not resolved.exists():
                broken.append((link, resolved))
            elif args.verbose:
                rel = path.relative_to(root)
                print(f"ok   {rel}:{link.line} -> {link.target}")

    for link, resolved in broken:
        try:
            source = link.source.relative_to(root)
        except ValueError:
            source = link.source
        print(f"BROKEN {source}:{link.line}: {link.target}")
        print(f"       expected: {os.path.normpath(resolved)}")

    print(
        f"\nscanned {len(files)} markdown files · "
        f"{checked} relative links checked · {skipped} external/anchor-only skipped"
    )
    print("note: anchors (FILE.md#section) are not validated, only the file part")
    if broken:
        print(f"result: BROKEN ({len(broken)})")
        return 1
    print("result: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
