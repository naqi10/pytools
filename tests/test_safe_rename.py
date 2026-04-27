from __future__ import annotations

import re
from pathlib import Path

import pytest

from pytools.files.safe_rename import apply, plan, undo


def test_plan_finds_matches(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("x")
    (tmp_path / "c.md").write_text("x")
    pairs = plan(tmp_path, re.compile(r"\.txt$"), ".rst")
    assert len(pairs) == 2
    assert all(new.suffix == ".rst" for _, new in pairs)


def test_apply_renames_and_writes_log(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello")
    pairs = plan(tmp_path, re.compile(r"\.txt$"), ".rst")
    log = tmp_path / "log.tsv"
    apply(pairs, log)
    assert (tmp_path / "a.rst").read_text() == "hello"
    assert not (tmp_path / "a.txt").exists()
    assert "a.txt\t" in log.read_text()


def test_undo_reverses(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello")
    pairs = plan(tmp_path, re.compile(r"\.txt$"), ".rst")
    log = tmp_path / "log.tsv"
    apply(pairs, log)
    n = undo(log)
    assert n == 1
    assert (tmp_path / "a.txt").read_text() == "hello"
    assert not log.exists()


def test_apply_refuses_collision(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("1")
    (tmp_path / "b.txt").write_text("2")
    # both renames target the same name
    pairs = [
        (tmp_path / "a.txt", tmp_path / "same.txt"),
        (tmp_path / "b.txt", tmp_path / "same.txt"),
    ]
    with pytest.raises(ValueError, match="collide"):
        apply(pairs, tmp_path / "log.tsv")


def test_apply_refuses_overwrite(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("new")
    (tmp_path / "a.bak").write_text("existing")
    pairs = [(tmp_path / "a.txt", tmp_path / "a.bak")]
    with pytest.raises(ValueError, match="overwrite"):
        apply(pairs, tmp_path / "log.tsv")
