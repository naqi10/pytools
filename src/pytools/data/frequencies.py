"""Count value frequencies at a JSON path across a JSON Lines stream.

Examples:
    cat events.jsonl | pytools-frequencies .event_type
    pytools-frequencies --top 10 .user.country < users.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable

from pytools.data.jq_lite import query


def count(stream: Iterable[str], path: str = ".") -> Counter[str]:
    """Count occurrences of values at `path` across JSON-per-line input."""
    counter: Counter[str] = Counter()
    for raw in stream:
        line = raw.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        for v in query(data, path):
            counter[json.dumps(v, ensure_ascii=False)] += 1
    return counter


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Count value frequencies in a JSONL stream.")
    p.add_argument("path", default=".", nargs="?")
    p.add_argument("--top", type=int, default=20)
    args = p.parse_args(argv)

    counter = count(sys.stdin, args.path)
    for value, n in counter.most_common(args.top):
        print(f"{n:>8}  {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
