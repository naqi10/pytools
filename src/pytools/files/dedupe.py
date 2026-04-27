"""Find duplicate files under a directory by SHA-256, grouped.

Examples:
    pytools-dedupe /path/to/dir
    pytools-dedupe . --min-size 1024
"""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def hash_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while data := f.read(chunk):
            h.update(data)
    return h.hexdigest()


def find_duplicates(root: Path, min_size: int = 1) -> dict[str, list[Path]]:
    """Return {sha256: [paths]} for any group of two or more identical files."""
    by_size: dict[int, list[Path]] = defaultdict(list)
    for p in root.rglob("*"):
        if p.is_file() and p.stat().st_size >= min_size:
            by_size[p.stat().st_size].append(p)
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        for p in paths:
            by_hash[hash_file(p)].append(p)
    return {h: ps for h, ps in by_hash.items() if len(ps) > 1}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Find duplicate files by content hash.")
    p.add_argument("root", type=Path)
    p.add_argument("--min-size", type=int, default=1, help="ignore files smaller than this")
    args = p.parse_args(argv)

    dupes = find_duplicates(args.root, args.min_size)
    for digest, paths in dupes.items():
        print(f"\n# {digest[:12]}  ({len(paths)} copies)")
        for path in paths:
            print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
