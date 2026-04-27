"""Tiny jq-like dotted-path query for JSON.

Examples:
    echo '{"a":{"b":[1,2,3]}}' | pytools-jq-lite .a.b[1]
    cat data.json | pytools-jq-lite '.users[].name'

Supports: `.key`, `[index]`, `[]` (splat). For full jq, use jq itself.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from typing import Any

_TOKEN = re.compile(r"\.([A-Za-z_][\w-]*)|\[(\d+)\]|\[\]")


def query(data: Any, path: str) -> Iterable[Any]:
    """Yield values at `path` within `data`."""
    if not path or path == ".":
        yield data
        return
    nodes: list[Any] = [data]
    for m in _TOKEN.finditer(path):
        key, idx = m.group(1), m.group(2)
        is_splat = m.group(0) == "[]"
        nxt: list[Any] = []
        for n in nodes:
            if key is not None:
                nxt.append(n[key])
            elif idx is not None:
                nxt.append(n[int(idx)])
            elif is_splat:
                nxt.extend(n)
        nodes = nxt
    yield from nodes


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Tiny jq-like JSON path query.")
    p.add_argument("path", default=".", nargs="?")
    args = p.parse_args(argv)

    data = json.load(sys.stdin)
    for value in query(data, args.path):
        print(json.dumps(value, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
