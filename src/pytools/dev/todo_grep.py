"""Find TODO/FIXME/XXX/HACK markers in a tree, grouped by tag.

Examples:
    pytools-todo-grep src/
    pytools-todo-grep --tags TODO,XXX .
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

DEFAULT_TAGS = ("TODO", "FIXME", "XXX", "HACK")
_BINARY_HINT = b"\x00"


def find_todos(
    root: Path,
    tags: tuple[str, ...] = DEFAULT_TAGS,
) -> dict[str, list[tuple[Path, int, str]]]:
    """Return {tag: [(path, line, message)]} across text files under `root`."""
    pattern = re.compile(rf"\b({'|'.join(tags)})\b[:\s]?\s*(.*)")
    out: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        try:
            data = p.read_bytes()
        except OSError:
            continue
        if _BINARY_HINT in data[:8000]:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            m = pattern.search(line)
            if m:
                out[m.group(1)].append((p, i, m.group(2).strip()))
    return dict(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Find TODO/FIXME/XXX/HACK markers.")
    p.add_argument("root", type=Path, nargs="?", default=Path())
    p.add_argument("--tags", default=",".join(DEFAULT_TAGS))
    args = p.parse_args(argv)

    tags = tuple(t.strip() for t in args.tags.split(",") if t.strip())
    grouped = find_todos(args.root, tags)
    for tag in tags:
        items = grouped.get(tag, [])
        if not items:
            continue
        print(f"\n# {tag}  ({len(items)})")
        for path, line, msg in items:
            print(f"  {path}:{line}: {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
