#!/usr/bin/env python3
"""
Train LoRA adapter for Outpost-Tiny on messages JSONL (tiny-lora-v0 / v1).

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
        default=ROOT / "datasets" / "tiny-lora-v1" / "train.messages.jsonl",
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
    p.add_argument(
        "--resume",
        type=Path,
        default=None,
        help="Resume from trainer checkpoint dir",
    )
    p.add_argument(
        "--dtype",
        choices=("auto", "float16", "float32"),
        default="auto",
        help="auto: float32 on cpu, float16 on mps/cuda (use float32 on MPS if NaNs)",
    )
    p.add_argument("--max-grad-norm", type=float, default=0.5)
    return p.parse_args()


def adapter_has_nan(adapter_dir: Path) -> bool:
    from safetensors import safe_open

    for f in adapter_dir.rglob("*.safetensors"):
        with safe_open(f, framework="pt") as s:
            for key in s.keys():
                if bool(s.get_tensor(key).isnan().any()):
                    return True
    return False


def _copy_adapter(src: Path, dst: Path) -> None:
    import shutil

    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


class NanGuardCallback:
    """Stop on NaN loss; keep last finite adapter under run_dir/adapter-last-good."""

    def __init__(self, run_dir: Path, trainer_ref: dict):
        self.run_dir = run_dir
        self.trainer_ref = trainer_ref
        self.last_good = run_dir / "adapter-last-good"
        self.stopped_for_nan = False

    def on_log(self, args, state, control, logs=None, **kwargs):  # noqa: ANN001
        import math

        if not logs:
            return
        loss = logs.get("loss")
        if loss is None:
            return
        if isinstance(loss, float) and (math.isnan(loss) or math.isinf(loss)):
            print(f"WARN: NaN/Inf loss at step {state.global_step} — stopping", flush=True)
            self.stopped_for_nan = True
            control.should_training_stop = True
            control.should_save = False

    def on_save(self, args, state, control, **kwargs):  # noqa: ANN001
        ckpt = Path(args.output_dir) / f"checkpoint-{state.global_step}"
        if not ckpt.is_dir():
            return
        if adapter_has_nan(ckpt):
            print(f"WARN: NaN weights in {ckpt.name} — stopping", flush=True)
            self.stopped_for_nan = True
            control.should_training_stop = True
            return
        trainer = self.trainer_ref.get("trainer")
        if trainer is None:
            return
        self.last_good.mkdir(parents=True, exist_ok=True)
        trainer.model.save_pretrained(self.last_good)
        if adapter_has_nan(self.last_good):
            print("WARN: last-good save became NaN — ignoring", flush=True)
            return
        print(f"last-good ← step {state.global_step}", flush=True)


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
        print(
            "Run: python3 scripts/build_tiny_lora_data.py --version v1",
            file=sys.stderr,
        )
        return 1

    # Late imports so --help works without torch installed
    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TrainerCallback,
    )
    from trl import SFTConfig, SFTTrainer

    class _NanGuard(NanGuardCallback, TrainerCallback):
        pass

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

    if args.dtype == "float32" or device == "cpu":
        torch_dtype = torch.float32
    elif args.dtype == "float16":
        torch_dtype = torch.float16
    else:
        # auto: float16 on mps/cuda to fit 3B; override with --dtype float32 if NaNs
        torch_dtype = torch.float16

    model_kwargs: dict = {
        "trust_remote_code": True,
        "dtype": torch_dtype if quant is None else None,
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

    if hasattr(model, "gradient_checkpointing_enable"):
        model.gradient_checkpointing_enable()
        if hasattr(model, "enable_input_require_grads"):
            model.enable_input_require_grads()

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
        save_strategy="steps",
        save_steps=1,
        save_total_limit=40,
        bf16=False,
        fp16=(device == "cuda" and quant is None),
        max_grad_norm=args.max_grad_norm,
        max_length=args.max_seq_len,
        report_to=[],
        seed=42,
        dataloader_pin_memory=False,
        dataloader_num_workers=0,
        gradient_checkpointing=True,
        optim="adamw_torch",
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

    trainer_ref: dict = {"trainer": trainer}
    nan_guard = _NanGuard(run_dir, trainer_ref)
    trainer.add_callback(nan_guard)

    # Avoid tokenizer parallelism warning noise
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    if device == "mps":
        os.environ.setdefault("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.0")

    if args.resume is not None:
        print(f"resume={args.resume}")
        trainer.train(resume_from_checkpoint=str(args.resume))
    else:
        trainer.train()

    adapter_dir.mkdir(parents=True, exist_ok=True)
    tokenizer.save_pretrained(adapter_dir)
    source = adapter_dir
    trainer.model.save_pretrained(adapter_dir)
    if adapter_has_nan(adapter_dir):
        good = run_dir / "adapter-last-good"
        if good.is_dir() and not adapter_has_nan(good):
            print(f"WARN: final adapter NaN — restoring {good}", flush=True)
            _copy_adapter(good, adapter_dir)
            source = good
        else:
            print(
                f"ERROR: adapter contains NaN weights → {adapter_dir}\n"
                "  Retry with: --lr 8e-5 --max-grad-norm 0.3 (MPS-stable)",
                file=sys.stderr,
            )
            return 3
    write_notes(run_dir, args, device, len(rows))

    print(f"OK adapter → {adapter_dir} (from {source.name})")
    print(f"OK notes   → {run_dir / 'NOTES.md'}")
    if nan_guard.stopped_for_nan:
        print("NOTE: training stopped early due to NaN; using last-good weights")
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
