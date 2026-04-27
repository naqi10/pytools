"""Top N files by churn (lines added + removed) in a git repo.

Examples:
    pytools-git-churn --since 30.days --top 10
    pytools-git-churn --since 2024-01-01 --repo /path/to/repo
"""

from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict


def churn(since: str, repo: str = ".") -> dict[str, int]:
    """Return {path: lines_added+removed} since `since`."""
    out = subprocess.run(
        ["git", "-C", repo, "log", f"--since={since}", "--numstat", "--format="],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    totals: dict[str, int] = defaultdict(int)
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 3 or "-" in parts[:2]:
            continue
        added, removed, path = parts
        totals[path] += int(added) + int(removed)
    return dict(totals)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Top files by git churn.")
    p.add_argument("--since", default="30.days")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--repo", default=".")
    args = p.parse_args(argv)

    totals = churn(args.since, args.repo)
    for path, lines in sorted(totals.items(), key=lambda kv: -kv[1])[: args.top]:
        print(f"{lines:>8}  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
