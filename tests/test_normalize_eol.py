from __future__ import annotations

from pathlib import Path

from pytools.files.normalize_eol import normalize


def test_crlf_to_lf(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_bytes(b"a\r\nb\r\nc\r\n")
    assert normalize(f, b"\n") is True
    assert f.read_bytes() == b"a\nb\nc\n"


def test_lf_to_crlf(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_bytes(b"a\nb\nc\n")
    assert normalize(f, b"\r\n") is True
    assert f.read_bytes() == b"a\r\nb\r\nc\r\n"


def test_already_correct_returns_false(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_bytes(b"a\nb\nc\n")
    assert normalize(f, b"\n") is False


def test_dry_run_does_not_modify(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_bytes(b"a\r\nb\r\n")
    assert normalize(f, b"\n", dry_run=True) is True
    assert f.read_bytes() == b"a\r\nb\r\n"


def test_skips_binary(tmp_path: Path) -> None:
    f = tmp_path / "x.bin"
    f.write_bytes(b"\x00\x01\x02\r\n")
    assert normalize(f, b"\n") is False
    assert f.read_bytes() == b"\x00\x01\x02\r\n"


def test_handles_mixed_endings(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_bytes(b"a\r\nb\nc\rd\n")
    normalize(f, b"\n")
    assert f.read_bytes() == b"a\nb\nc\nd\n"
