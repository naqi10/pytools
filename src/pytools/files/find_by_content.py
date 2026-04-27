"""Recursive grep — find lines containing a pattern, skipping binary files.

Examples:
    pytools-find-content "TODO" src/
    pytools-find-content --regex "def\\s+main" .
    pytools-find-content -i "error" logs/
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterator
from pathlib import Path

_BINARY_HINT = b"\x00"


def search(root: Path, pattern: re.Pattern[str]) -> Iterator[tuple[Path, int, str]]:
    """Yield (path, line_number, line) for every match under `root`."""
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
            if pattern.search(line):
                yield p, i, line


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Recursive grep, binary-skipping.")
    p.add_argument("pattern")
    p.add_argument("root", type=Path, nargs="?", default=Path())
    p.add_argument("--regex", action="store_true", help="treat pattern as a regex")
    p.add_argument("-i", "--ignore-case", action="store_true")
    args = p.parse_args(argv)

    raw = args.pattern if args.regex else re.escape(args.pattern)
    flags = re.IGNORECASE if args.ignore_case else 0
    compiled = re.compile(raw, flags)

    found = 0
    for path, line, content in search(args.root, compiled):
        print(f"{path}:{line}: {content}")
        found += 1
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
