"""Normalize text-file line endings to LF, CRLF, or CR.

Examples:
    pytools-normalize-eol --to lf src/
    pytools-normalize-eol --to crlf --dry-run docs/
"""

from __future__ import annotations

import argparse
from pathlib import Path

_BINARY_HINT = b"\x00"
_ENDINGS: dict[str, bytes] = {"lf": b"\n", "crlf": b"\r\n", "cr": b"\r"}


def normalize(path: Path, ending: bytes, *, dry_run: bool = False) -> bool:
    """Rewrite `path` with target line `ending`. Return True if it would change."""
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if _BINARY_HINT in data[:8000]:
        return False
    lf = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    new = lf if ending == b"\n" else lf.replace(b"\n", ending)
    if new == data:
        return False
    if not dry_run:
        path.write_bytes(new)
    return True


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Normalize line endings under a tree.")
    p.add_argument("root", type=Path)
    p.add_argument("--to", choices=("lf", "crlf", "cr"), default="lf")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    target = _ENDINGS[args.to]
    files = [args.root] if args.root.is_file() else [f for f in args.root.rglob("*") if f.is_file()]
    changed = 0
    for f in files:
        if normalize(f, target, dry_run=args.dry_run):
            verb = "would normalize" if args.dry_run else "normalized"
            print(f"{verb}: {f}")
            changed += 1
    print(f"\n{changed} file(s) {'would be ' if args.dry_run else ''}changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
