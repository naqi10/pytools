from __future__ import annotations

from pathlib import Path

from pytools.files.dedupe import find_duplicates, hash_file


def test_finds_duplicate_pair(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("hello")
    (tmp_path / "c.txt").write_text("different")
    dupes = find_duplicates(tmp_path)
    assert len(dupes) == 1
    only = next(iter(dupes.values()))
    assert {p.name for p in only} == {"a.txt", "b.txt"}


def test_no_dupes_returns_empty(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("one")
    (tmp_path / "b.txt").write_text("two")
    assert find_duplicates(tmp_path) == {}


def test_min_size_filters_small_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("x")
    assert find_duplicates(tmp_path, min_size=10) == {}


def test_recurses_into_subdirs(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("payload")
    sub = tmp_path / "nested" / "deep"
    sub.mkdir(parents=True)
    (sub / "b.txt").write_text("payload")
    dupes = find_duplicates(tmp_path)
    assert len(dupes) == 1


def test_hash_file_is_sha256(tmp_path: Path) -> None:
    f = tmp_path / "x.bin"
    f.write_bytes(b"abc")
    assert hash_file(f) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
