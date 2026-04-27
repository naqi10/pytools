"""Lint a .env file: duplicates, missing equals, unquoted spaces, empty values.

Examples:
    pytools-env-lint .env
    pytools-env-lint .env.production
"""

from __future__ import annotations

import argparse
from pathlib import Path


def lint_env(text: str) -> list[tuple[int, str]]:
    """Return [(line_number, problem)] for issues found in a .env file body."""
    issues: list[tuple[int, str]] = []
    seen: dict[str, int] = {}
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            issues.append((i, f"missing '=' in: {line}"))
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            issues.append((i, "empty key"))
            continue
        if key in seen:
            issues.append((i, f"duplicate key '{key}' (first defined on line {seen[key]})"))
        else:
            seen[key] = i
        if not value.strip():
            issues.append((i, f"empty value for '{key}'"))
        elif " " in value and not (value.startswith('"') or value.startswith("'")):
            issues.append((i, f"unquoted space in value of '{key}'"))
    return issues


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lint a .env file.")
    p.add_argument("path", type=Path)
    args = p.parse_args(argv)

    issues = lint_env(args.path.read_text(encoding="utf-8"))
    for line, problem in issues:
        print(f"{args.path}:{line}: {problem}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
