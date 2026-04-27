"""Diff the inferred schema of two JSON documents.

Examples:
    pytools-schema-diff old.json new.json

Reports added (`+`), removed (`-`), and type-changed (`~`) paths.
For arrays, the schema of the first element is used as representative.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

_TYPES: tuple[tuple[type, str], ...] = (
    # bool must come before int because bool is a subclass of int
    (bool, "bool"),
    (int, "int"),
    (float, "float"),
    (str, "string"),
    (list, "array"),
    (dict, "object"),
)


def _type(v: Any) -> str:
    if v is None:
        return "null"
    for cls, name in _TYPES:
        if isinstance(v, cls):
            return name
    return "unknown"


def schema(value: Any, path: str = "") -> dict[str, str]:
    """Return {dotted_path: type_name} for every leaf and container."""
    out: dict[str, str] = {path or ".": _type(value)}
    if isinstance(value, dict):
        for k, v in value.items():
            out.update(schema(v, f"{path}.{k}" if path else k))
    elif isinstance(value, list) and value:
        out.update(schema(value[0], f"{path}[]"))
    return out


def diff(old: dict[str, str], new: dict[str, str]) -> list[str]:
    """Return human-readable diff lines."""
    out: list[str] = []
    for k in sorted(set(old) | set(new)):
        a, b = old.get(k), new.get(k)
        if a is None:
            out.append(f"+ {k}: {b}")
        elif b is None:
            out.append(f"- {k}: {a}")
        elif a != b:
            out.append(f"~ {k}: {a} -> {b}")
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Diff inferred schemas of two JSON files.")
    p.add_argument("old", type=Path)
    p.add_argument("new", type=Path)
    args = p.parse_args(argv)

    old = schema(json.loads(args.old.read_text(encoding="utf-8")))
    new = schema(json.loads(args.new.read_text(encoding="utf-8")))
    changes = diff(old, new)
    for line in changes:
        print(line)
    return 1 if changes else 0


if __name__ == "__main__":
    raise SystemExit(main())
