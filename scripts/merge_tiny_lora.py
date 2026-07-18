#!/usr/bin/env python3
"""
Merge PEFT LoRA adapter into base HF weights for GGUF conversion.

Example:
  python3 scripts/merge_tiny_lora.py \\
    --adapter artifacts/runs/20260718-120000/adapter \\
    --out artifacts/hf/outpost-tiny-v0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Merge Tiny LoRA into full HF model")
    p.add_argument("--adapter", type=Path, required=True, help="PEFT adapter dir")
    p.add_argument(
        "--base",
        default="Qwen/Qwen2.5-3B-Instruct",
        help="Same base used for train",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=ROOT / "artifacts" / "hf" / "outpost-tiny-v0",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.adapter.is_dir():
        print(f"ERROR: adapter not found: {args.adapter}", file=sys.stderr)
        return 1

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"base={args.base} adapter={args.adapter} out={args.out}")
    tokenizer = AutoTokenizer.from_pretrained(args.adapter, trust_remote_code=True)
    base = AutoModelForCausalLM.from_pretrained(
        args.base,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map="cpu",
    )
    model = PeftModel.from_pretrained(base, str(args.adapter))
    merged = model.merge_and_unload()
    args.out.mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(args.out, safe_serialization=True)
    tokenizer.save_pretrained(args.out)
    print(f"OK merged HF → {args.out}")
    print("Next: convert to GGUF — docs/TRAIN-TINY-LORA.md § Export")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ImportError as e:
        print("ERROR: missing deps:", e, file=sys.stderr)
        print("  pip install -r requirements-train.txt", file=sys.stderr)
        raise SystemExit(2)
