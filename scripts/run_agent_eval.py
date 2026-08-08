#!/usr/bin/env python3
"""Run agent-v0 prompts against local Outpost; write raw JSONL for scoring.

Example:
  # sovereignd config/sovereign.agent-eval.toml on :8097
  python3 scripts/run_agent_eval.py --out eval/results/raw/agent-v0-<tag>/
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", type=Path, default=ROOT / "eval/prompts/agent-v0.jsonl")
    ap.add_argument("--base-url", default="http://127.0.0.1:8097/v1")
    ap.add_argument("--model", default="outpost-tiny-hammer")
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--max-tokens", type=int, default=256)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = args.out or (ROOT / "eval/results/raw" / f"agent-v0-{stamp}")
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    for line in args.prompts.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        p = json.loads(line)
        pid = p.get("id") or p.get("name")
        user = p.get("prompt") or p.get("user") or p["messages"][-1]["content"]
        print(f"ASK {pid}…", flush=True)
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
        row = {"id": pid, "user": user, "answer": answer, "error": err, "meta": p}
        rows.append(row)
        (out / f"{pid}.txt").write_text(answer or f"ERROR: {err}", encoding="utf-8")

    (out / "all.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    meta = {
        "base_url": args.base_url,
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "prompts": str(args.prompts),
        "n": len(rows),
        "stamp": stamp,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(rows)} prompts)")


if __name__ == "__main__":
    main()
