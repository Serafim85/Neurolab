"""Data prep for scripts/train_mlx_lora.py — no mlx import."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from train_mlx_lora import prepare_mlx_data


def test_prepare_mlx_data(tmp_path: Path) -> None:
    src = tmp_path / "train.messages.jsonl"
    rows = [
        {"tag": "a", "messages": [{"role": "user", "content": "u1"}, {"role": "assistant", "content": "a1"}]},
        {"tag": "b", "messages": [{"role": "user", "content": "u2"}, {"role": "assistant", "content": "a2"}]},
    ]
    src.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    n = prepare_mlx_data(src, tmp_path / "mlx")
    assert n == 2
    train = (tmp_path / "mlx" / "train.jsonl").read_text(encoding="utf-8").strip().splitlines()
    valid = (tmp_path / "mlx" / "valid.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(train) == 2
    assert len(valid) == 1
    assert json.loads(valid[0])["tag"] == "b"


def test_prepare_mlx_data_rejects_empty(tmp_path: Path) -> None:
    src = tmp_path / "empty.jsonl"
    src.write_text("\n", encoding="utf-8")
    with pytest.raises(ValueError):
        prepare_mlx_data(src, tmp_path / "mlx")
