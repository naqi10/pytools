"""Bulk regex rename with a written undo log. Refuses to overwrite or collide.

Examples:
    pytools-safe-rename '\\.txt$' '.md' src/
    pytools-safe-rename --dry-run '^old_' 'new_' .
    pytools-safe-rename --undo .pytools-rename.log

The undo log is a TSV (old<TAB>new) written under the working root.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LOG_NAME = ".pytools-rename.log"


def plan(root: Path, pattern: re.Pattern[str], replacement: str) -> list[tuple[Path, Path]]:
    """Return [(old, new)] for all files whose names would change."""
    pairs: list[tuple[Path, Path]] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        new_name = pattern.sub(replacement, p.name)
        if new_name != p.name:
            pairs.append((p, p.with_name(new_name)))
    return pairs


def apply(pairs: list[tuple[Path, Path]], log: Path) -> None:
    """Perform renames, writing the undo log. Raises on collision or overwrite."""
    targets = [new for _, new in pairs]
    if len(set(targets)) != len(targets):
        raise ValueError("rename targets collide; refusing to apply")
    olds = {old for old, _ in pairs}
    overwrites = [new for new in targets if new.exists() and new not in olds]
    if overwrites:
        raise ValueError(f"would overwrite existing files: {overwrites[:3]}")
    with log.open("w", encoding="utf-8") as f:
        for old, new in pairs:
            old.rename(new)
            f.write(f"{old}\t{new}\n")


def undo(log: Path) -> int:
    """Reverse the renames recorded in `log`. Returns count reversed."""
    pairs: list[tuple[str, str]] = []
    with log.open(encoding="utf-8") as f:
        for line in f:
            old, _, new = line.rstrip("\n").partition("\t")
            pairs.append((old, new))
    for old, new in reversed(pairs):
        Path(new).rename(Path(old))
    log.unlink()
    return len(pairs)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Bulk regex rename with undo log.")
    p.add_argument("--undo", type=Path, help="apply the undo log at this path")
    p.add_argument("pattern", nargs="?")
    p.add_argument("replacement", nargs="?")
    p.add_argument("root", type=Path, nargs="?", default=Path())
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    if args.undo:
        n = undo(args.undo)
        print(f"undone {n} renames")
        return 0

    if args.pattern is None or args.replacement is None:
        print("error: pattern and replacement required (or use --undo)", file=sys.stderr)
        return 2

    pairs = plan(args.root, re.compile(args.pattern), args.replacement)
    for old, new in pairs:
        print(f"{old} -> {new}")
    if args.dry_run or not pairs:
        return 0
    log = args.root / LOG_NAME
    apply(pairs, log)
    print(f"\nundo with: pytools-safe-rename --undo {log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
