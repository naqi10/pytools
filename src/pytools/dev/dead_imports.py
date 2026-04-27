"""Find imports that are not referenced in the same file (likely dead).

Examples:
    pytools-dead-imports src/
    pytools-dead-imports myfile.py

Heuristic only — does not catch dynamic uses (`getattr`, `__all__`,
re-exports, string annotations under `from __future__ import annotations`).
For canonical results, use ruff's F401.
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path


def dead_imports(source: str) -> list[tuple[int, str]]:
    """Return [(line, name)] of imports not referenced by name in the source."""
    tree = ast.parse(source)
    imports: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((node.lineno, alias.asname or alias.name.split(".")[0]))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                imports.append((node.lineno, alias.asname or alias.name))

    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            n: ast.expr = node
            while isinstance(n, ast.Attribute):
                n = n.value
            if isinstance(n, ast.Name):
                used.add(n.id)
    return [(line, name) for line, name in imports if name not in used]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Find unused imports (heuristic).")
    p.add_argument("path", type=Path)
    args = p.parse_args(argv)

    files = [args.path] if args.path.is_file() else list(args.path.rglob("*.py"))
    found = 0
    for f in files:
        for line, name in dead_imports(f.read_text(encoding="utf-8")):
            print(f"{f}:{line}: unused import '{name}'")
            found += 1
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
