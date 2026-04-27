from __future__ import annotations

from pathlib import Path

from pytools.dev.todo_grep import find_todos


def test_finds_basic_tags(tmp_path: Path) -> None:
    f = tmp_path / "a.py"
    f.write_text("x = 1  # TODO: refactor this\ny = 2  # FIXME urgent\n")
    out = find_todos(tmp_path)
    assert "TODO" in out
    assert "FIXME" in out
    assert out["TODO"][0][2] == "refactor this"


def test_groups_by_tag(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("# TODO one\n# TODO two\n# XXX three\n")
    out = find_todos(tmp_path)
    assert len(out["TODO"]) == 2
    assert len(out["XXX"]) == 1


def test_skips_binary(tmp_path: Path) -> None:
    (tmp_path / "binary.bin").write_bytes(b"\x00\x01\x02 TODO never\n")
    (tmp_path / "good.txt").write_text("# TODO yes\n")
    out = find_todos(tmp_path)
    assert len(out.get("TODO", [])) == 1
    assert out["TODO"][0][0].name == "good.txt"


def test_custom_tags(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("# TODO a\n# REVIEW b\n")
    out = find_todos(tmp_path, tags=("REVIEW",))
    assert "REVIEW" in out
    assert "TODO" not in out
