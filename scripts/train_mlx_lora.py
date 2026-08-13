#!/usr/bin/env python3
"""Train LoRA on Qwen2.5-7B-Instruct via MLX, optionally fuse and export GGUF.

Apple Silicon path for NL-ADR-028. Does not use PEFT/CUDA QLoRA.

  python3 scripts/train_mlx_lora.py
  python3 scripts/train_mlx_lora.py --data datasets/tiny-lora-hammer2/train.messages.jsonl
  python3 scripts/train_mlx_lora.py --export-gguf   # fuse --dequantize + llama.cpp

Requires: mlx, mlx-lm (see docs/MLX-7B-PROBE.md). llama.cpp for --export-gguf.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "datasets" / "tiny-lora-hammer2" / "train.messages.jsonl"
DEFAULT_MODEL = "mlx-community/Qwen2.5-7B-Instruct-4bit"
LLAMA_CPP = Path(os.environ.get("LLAMA_CPP", Path.home() / "Projects" / "llama.cpp"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MLX LoRA for Outpost 7B (NL-ADR-028)")
    p.add_argument("--data", type=Path, default=DEFAULT_DATA)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--out", type=Path, default=None, help="Run dir (default artifacts/runs/<stamp>-mlx)")
    p.add_argument("--epochs", type=float, default=2.0)
    p.add_argument("--iters", type=int, default=None, help="Override iters (default: n_train * epochs)")
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--max-seq-len", type=int, default=512)
    p.add_argument("--num-layers", type=int, default=16, help="-1 = all layers")
    p.add_argument("--lr", type=float, default=1e-5)
    p.add_argument("--python", default=sys.executable)
    p.add_argument(
        "--resume-adapter",
        type=Path,
        default=None,
        help="mlx-lm --resume-adapter-file (e.g. prior adapters.safetensors)",
    )
    p.add_argument(
        "--export-gguf",
        action="store_true",
        help="After train: fuse --dequantize, convert_hf_to_gguf, llama-quantize Q4_K_M",
    )
    p.add_argument("--skip-train", action="store_true", help="Only export from existing --out/adapter")
    return p.parse_args()


def prepare_mlx_data(src: Path, dst: Path) -> int:
    """Copy messages JSONL into mlx-lm {train,valid}.jsonl. Returns n_train."""
    if not src.is_file():
        raise FileNotFoundError(src)
    lines = [ln for ln in src.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        raise ValueError(f"empty dataset: {src}")
    for ln in lines:
        obj = json.loads(ln)
        if "messages" not in obj:
            raise ValueError(f"{src} line missing 'messages'")
    dst.mkdir(parents=True, exist_ok=True)
    (dst / "train.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    valid = lines[-1] if len(lines) == 1 else lines[-1]
    (dst / "valid.jsonl").write_text(valid + "\n", encoding="utf-8")
    return len(lines)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=cwd)


def write_notes(run_dir: Path, args: argparse.Namespace, n_train: int, iters: int) -> None:
    text = "\n".join(
        [
            f"# MLX LoRA run {run_dir.name}",
            "",
            f"- time: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}",
            f"- base: `{args.model}` (NL-ADR-028, Apache-2.0)",
            f"- data: `{args.data}` (n={n_train})",
            f"- iters: {iters} · batch {args.batch_size} · seq {args.max_seq_len} · layers {args.num_layers}",
            f"- adapter: `{run_dir / 'adapter'}`",
            f"- resume: `{args.resume_adapter}`" if args.resume_adapter else "- resume: none",
            "- 3B GGUFs on disk remain research-only; do not ship them commercially.",
            "",
        ]
    )
    (run_dir / "NOTES.md").write_text(text, encoding="utf-8")


def export_gguf(args: argparse.Namespace, run_dir: Path) -> None:
    adapter = run_dir / "adapter"
    fused = run_dir / "fused"
    gguf_f16 = ROOT / "artifacts" / f"{run_dir.name}.f16.gguf"
    gguf_q4 = ROOT / "artifacts" / f"{run_dir.name}.Q4_K_M.gguf"
    convert = LLAMA_CPP / "convert_hf_to_gguf.py"
    quant = LLAMA_CPP / "build" / "bin" / "llama-quantize"
    if not convert.is_file():
        raise FileNotFoundError(f"llama.cpp convert missing: {convert}")
    if not quant.is_file():
        raise FileNotFoundError(f"llama-quantize missing: {quant}")

    # mlx_lm fuse --export-gguf rejects model_type qwen2. Dequantize to HF-like dir, then convert.
    run(
        [
            args.python,
            "-m",
            "mlx_lm",
            "fuse",
            "--model",
            args.model,
            "--adapter-path",
            str(adapter),
            "--save-path",
            str(fused),
            "--dequantize",
        ]
    )
    convert_py = os.environ.get("CONVERT_PYTHON", str(ROOT / ".venv" / "bin" / "python3"))
    if not Path(convert_py).is_file():
        convert_py = args.python
    run(
        [
            convert_py,
            str(convert),
            str(fused),
            "--outfile",
            str(gguf_f16),
        ]
    )
    run([str(quant), str(gguf_f16), str(gguf_q4), "Q4_K_M"])
    digest = subprocess.check_output(["shasum", "-a", "256", str(gguf_q4)], text=True)
    (gguf_q4.with_suffix(gguf_q4.suffix + ".SHA256.txt")).write_text(digest, encoding="utf-8")
    print(digest, end="")
    print(
        "Fused FP16 GGUF is large; delete after Q4 if disk is tight:\n"
        f"  rm {gguf_f16}",
        file=sys.stderr,
    )


def main() -> int:
    args = parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = args.out or (ROOT / "artifacts" / "runs" / f"{stamp}-mlx")
    run_dir = run_dir.resolve()
    adapter = run_dir / "adapter"
    data_dir = run_dir / "mlx-data"

    n_train = 0
    if args.data.is_file():
        n_train = sum(1 for ln in args.data.read_text(encoding="utf-8").splitlines() if ln.strip())
    iters = args.iters if args.iters is not None else max(int(n_train * args.epochs), 1)

    run_dir.mkdir(parents=True, exist_ok=True)

    if not args.skip_train:
        n_train = prepare_mlx_data(args.data, data_dir)
        iters = args.iters if args.iters is not None else max(int(n_train * args.epochs), 1)
        adapter.mkdir(parents=True, exist_ok=True)
        cmd = [
            args.python,
            "-m",
            "mlx_lm",
            "lora",
            "--model",
            args.model,
            "--train",
            "--data",
            str(data_dir),
            "--adapter-path",
            str(adapter),
            "--iters",
            str(iters),
            "--batch-size",
            str(args.batch_size),
            "--max-seq-length",
            str(args.max_seq_len),
            "--num-layers",
            str(args.num_layers),
            "--learning-rate",
            str(args.lr),
            "--grad-checkpoint",
            "--steps-per-report",
            "10",
            "--steps-per-eval",
            str(max(iters, 1)),
            "--val-batches",
            "1",
        ]
        if args.resume_adapter is not None:
            resume = args.resume_adapter.expanduser().resolve()
            if not resume.is_file():
                raise FileNotFoundError(f"resume adapter missing: {resume}")
            cmd += ["--resume-adapter-file", str(resume)]
        run(cmd)
        write_notes(run_dir, args, n_train, iters)
        print(f"OK adapter → {adapter}")
    else:
        if not (adapter / "adapters.safetensors").is_file():
            print(f"ERROR: no adapter at {adapter}", file=sys.stderr)
            return 1

    if args.export_gguf:
        export_gguf(args, run_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as e:
        print(f"ERROR: command failed ({e.returncode})", file=sys.stderr)
        raise SystemExit(e.returncode)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
