#!/usr/bin/env python3
"""
Train LoRA adapter for Outpost-Tiny on tiny-lora-v0 (messages JSONL).

Example:
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r requirements-train.txt
  python3 scripts/train_tiny_lora.py

Outputs:
  artifacts/runs/<stamp>/adapter/   — PEFT adapter
  artifacts/runs/<stamp>/NOTES.md   — run card for agents
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Outpost-Tiny LoRA train (PEFT + TRL)")
    p.add_argument(
        "--data",
        type=Path,
        default=ROOT / "datasets" / "tiny-lora-v0" / "train.messages.jsonl",
    )
    p.add_argument(
        "--base",
        default="Qwen/Qwen2.5-3B-Instruct",
        help="HF model id or local path",
    )
    p.add_argument("--out", type=Path, default=None, help="Run dir (default artifacts/runs/<stamp>)")
    p.add_argument("--epochs", type=float, default=2.0)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--max-seq-len", type=int, default=1024)
    p.add_argument("--lora-r", type=int, default=16)
    p.add_argument("--lora-alpha", type=int, default=32)
    p.add_argument("--lora-dropout", type=float, default=0.05)
    p.add_argument(
        "--device",
        choices=("auto", "cuda", "mps", "cpu"),
        default="auto",
        help="auto: cuda > mps > cpu",
    )
    p.add_argument(
        "--load-in-4bit",
        action="store_true",
        help="QLoRA (CUDA + bitsandbytes only; ignore on Mac)",
    )
    return p.parse_args()


def pick_device(name: str) -> str:
    import torch

    if name != "auto":
        return name
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_messages_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if "messages" not in obj:
                raise ValueError(f"{path}:{line_no} missing messages")
            rows.append({"messages": obj["messages"], "tag": obj.get("tag", "")})
    if not rows:
        raise ValueError(f"empty dataset: {path}")
    return rows


def write_notes(
    run_dir: Path,
    args: argparse.Namespace,
    device: str,
    n_examples: int,
) -> None:
    stamp = run_dir.name
    text = f"""# Run {stamp}

| Field | Value |
|---|---|
| date_utc | {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} |
| base | `{args.base}` |
| data | `{args.data}` |
| n_examples | {n_examples} |
| device | {device} |
| epochs | {args.epochs} |
| lr | {args.lr} |
| batch_size | {args.batch_size} |
| grad_accum | {args.grad_accum} |
| max_seq_len | {args.max_seq_len} |
| lora_r | {args.lora_r} |
| lora_alpha | {args.lora_alpha} |
| load_in_4bit | {args.load_in_4bit} |
| adapter | `{run_dir / "adapter"}` |

## Next

```bash
python3 scripts/merge_tiny_lora.py --adapter {run_dir / "adapter"}
# then convert HF → GGUF (llama.cpp) — see docs/TRAIN-TINY-LORA.md
```

## Canon

- LoRA (Hu et al.) · Instruct-style post-train · CONTOUR-EGRESS
"""
    (run_dir / "NOTES.md").write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not args.data.is_file():
        print(f"ERROR: data not found: {args.data}", file=sys.stderr)
        print("Run: python3 scripts/build_tiny_lora_data.py", file=sys.stderr)
        return 1

    # Late imports so --help works without torch installed
    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from trl import SFTConfig, SFTTrainer

    device = pick_device(args.device)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = args.out or (ROOT / "artifacts" / "runs" / stamp)
    adapter_dir = run_dir / "adapter"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows = load_messages_jsonl(args.data)
    print(f"examples={len(rows)} base={args.base} device={device} out={run_dir}")

    tokenizer = AutoTokenizer.from_pretrained(args.base, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quant = None
    torch_dtype = torch.float16
    if args.load_in_4bit:
        if device != "cuda":
            print("WARN: --load-in-4bit ignored (needs CUDA + bitsandbytes)", file=sys.stderr)
        else:
            quant = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

    if device == "cpu":
        torch_dtype = torch.float32

    model_kwargs: dict = {
        "trust_remote_code": True,
        "torch_dtype": torch_dtype if quant is None else None,
    }
    if quant is not None:
        model_kwargs["quantization_config"] = quant
        model_kwargs["device_map"] = "auto"
    elif device == "cuda":
        model_kwargs["device_map"] = "auto"
    # MPS/CPU: load then .to(device)

    model = AutoModelForCausalLM.from_pretrained(args.base, **model_kwargs)
    if quant is None and device in ("mps", "cpu"):
        model = model.to(device)

    # Qwen2 target modules
    lora = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
    )

    def formatting(example: dict) -> str:
        return tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )

    ds = Dataset.from_list(rows)

    # trl API differs slightly across versions — use compatible SFTConfig fields
    sft_kwargs = dict(
        output_dir=str(run_dir / "trainer"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        logging_steps=1,
        save_strategy="epoch",
        bf16=False,
        fp16=(device == "cuda" and quant is None),
        max_length=args.max_seq_len,
        report_to=[],
        seed=42,
    )
    # Older trl used max_seq_length
    try:
        sft_config = SFTConfig(**sft_kwargs)
    except TypeError:
        sft_kwargs.pop("max_length", None)
        sft_kwargs["max_seq_length"] = args.max_seq_len
        sft_config = SFTConfig(**sft_kwargs)

    trainer_kwargs = dict(
        model=model,
        args=sft_config,
        train_dataset=ds,
        peft_config=lora,
        processing_class=tokenizer,
    )
    try:
        trainer = SFTTrainer(
            **trainer_kwargs,
            formatting_func=formatting,
        )
    except TypeError:
        # Newer trl: dataset already messages + chat template via tokenizer
        trainer = SFTTrainer(
            model=model,
            args=sft_config,
            train_dataset=ds,
            peft_config=lora,
            processing_class=tokenizer,
        )

    # Avoid tokenizer parallelism warning noise
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    trainer.train()
    adapter_dir.mkdir(parents=True, exist_ok=True)
    trainer.model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    write_notes(run_dir, args, device, len(rows))

    print(f"OK adapter → {adapter_dir}")
    print(f"OK notes   → {run_dir / 'NOTES.md'}")
    print("Next: python3 scripts/merge_tiny_lora.py --adapter", adapter_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ImportError as e:
        print("ERROR: missing train deps:", e, file=sys.stderr)
        print("  python3 -m venv .venv && source .venv/bin/activate", file=sys.stderr)
        print("  pip install -r requirements-train.txt", file=sys.stderr)
        raise SystemExit(2)
