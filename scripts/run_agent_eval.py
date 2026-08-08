#!/usr/bin/env python3
"""Run agent-v0 prompts against local Outpost; write raw JSONL for scoring.

Example:
  # sovereignd config/sovereign.agent-eval.toml on :8097
  python3 scripts/run_agent_eval.py --out eval/results/raw/agent-v0-<tag>/
  python3 scripts/run_agent_eval.py --repeats 5 --out eval/results/raw/agent-v0-<tag>/

Default sampling is greedy (temperature 0.0). With --repeats > 1 every prompt is
asked N times and each row carries a `repeat` index, so score_agent_eval.py can
report mean +- stdev instead of a single number.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def chat(base: str, model: str, user: str, *, temperature: float, max_tokens: int) -> str:
    url = base.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": user}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    ).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read().decode())
    return str(payload["choices"][0]["message"]["content"])


def load_prompts(path: Path) -> list[dict]:
    prompts = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        prompts.append(json.loads(line))
    return prompts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", type=Path, default=ROOT / "eval/prompts/agent-v0.jsonl")
    ap.add_argument("--base-url", default="http://127.0.0.1:8097/v1")
    ap.add_argument("--model", default="outpost-tiny-hammer")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-tokens", type=int, default=256)
    ap.add_argument("--repeats", type=int, default=1, help="ask every prompt N times")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if args.repeats < 1:
        ap.error("--repeats must be >= 1")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = args.out or (ROOT / "eval/results/raw" / f"agent-v0-{stamp}")
    out.mkdir(parents=True, exist_ok=True)

    prompts = load_prompts(args.prompts)
    rows = []
    for repeat in range(args.repeats):
        for p in prompts:
            pid = p.get("id") or p.get("name")
            user = p.get("prompt") or p.get("user") or p["messages"][-1]["content"]
            tag = pid if args.repeats == 1 else f"{pid} r{repeat}"
            print(f"ASK {tag}…", flush=True)
            try:
                answer = chat(
                    args.base_url,
                    args.model,
                    user,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                )
                err = None
            except Exception as exc:  # noqa: BLE001
                answer = ""
                err = str(exc)
            rows.append(
                {"id": pid, "repeat": repeat, "user": user, "answer": answer, "error": err, "meta": p}
            )
            name = f"{pid}.txt" if repeat == 0 else f"{pid}.r{repeat}.txt"
            (out / name).write_text(answer or f"ERROR: {err}", encoding="utf-8")

    (out / "all.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    meta = {
        "base_url": args.base_url,
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "repeats": args.repeats,
        "prompts": str(args.prompts),
        "n": len(prompts),
        "rows": len(rows),
        "stamp": stamp,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(prompts)} prompts × {args.repeats} repeat(s) = {len(rows)} rows)")
    print(f"score: python3 scripts/score_agent_eval.py {out}")


if __name__ == "__main__":
    main()
