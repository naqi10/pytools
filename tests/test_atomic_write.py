from __future__ import annotations

from pathlib import Path

import pytest

from pytools.files.atomic_write import atomic_write


def test_writes_file(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"
    with atomic_write(target) as f:
        f.write("hello")
    assert target.read_text() == "hello"


def test_overwrites_existing(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"
    target.write_text("old")
    with atomic_write(target) as f:
        f.write("new")
    assert target.read_text() == "new"


def test_rolls_back_on_error(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"
    target.write_text("original")
    with pytest.raises(RuntimeError, match="boom"), atomic_write(target) as f:
        f.write("partial")
        raise RuntimeError("boom")
    assert target.read_text() == "original"
    assert list(tmp_path.glob("*.tmp")) == []


def test_binary_mode(tmp_path: Path) -> None:
    target = tmp_path / "out.bin"
    with atomic_write(target, "wb") as f:
        f.write(b"\x00\x01\x02")
    assert target.read_bytes() == b"\x00\x01\x02"
