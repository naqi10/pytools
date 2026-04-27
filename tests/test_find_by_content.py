from __future__ import annotations

import re
from pathlib import Path

from pytools.files.find_by_content import search


def test_finds_literal_match(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("apple\nbanana\ncherry\n")
    matches = list(search(tmp_path, re.compile(re.escape("banana"))))
    assert len(matches) == 1
    assert matches[0][1] == 2
    assert matches[0][2] == "banana"


def test_regex_match(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def foo():\n    pass\ndef bar():\n    pass\n")
    matches = list(search(tmp_path, re.compile(r"def\s+\w+")))
    assert len(matches) == 2


def test_skips_binary(tmp_path: Path) -> None:
    (tmp_path / "bin.dat").write_bytes(b"\x00\x01 needle\n")
    (tmp_path / "txt.txt").write_text("needle in text\n")
    matches = list(search(tmp_path, re.compile("needle")))
    assert len(matches) == 1
    assert matches[0][0].name == "txt.txt"


def test_recurses(tmp_path: Path) -> None:
    sub = tmp_path / "deep" / "nest"
    sub.mkdir(parents=True)
    (sub / "x.txt").write_text("findme\n")
    matches = list(search(tmp_path, re.compile("findme")))
    assert len(matches) == 1
