# Contributing

## Adding a new tool

1. Pick a **category** (`dev`, `files`, `data`, `web`) — or propose a new one.
2. Create `src/pytools/<category>/<your_tool>.py` following the shape below.
3. Create `tests/test_<your_tool>.py` covering the public function (not the CLI).
4. Add a `pytools-<your-tool>` entry to `[project.scripts]` in `pyproject.toml`.
5. Add a row to the README and the matching docs page.

## The shape every tool follows

```python
"""One-line summary.

Longer description, examples, library usage.
"""

from __future__ import annotations

import argparse


def the_thing(...) -> ...:
    """Public function — this is what tests cover."""
    ...


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="...")
    # add args
    args = p.parse_args(argv)
    # call the_thing(args.x, args.y)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Quality gates

```bash
pytest                # all tests pass
ruff check .          # zero lint errors
ruff format --check . # formatted
mypy                  # zero type errors (strict mode)
```

CI runs the matrix on Python 3.10–3.13 across Linux, macOS, and Windows.

## Constraints

- **No runtime dependencies** unless absolutely necessary. Make the case in your PR.
- **Cross-platform** — if it can't run on Windows, document that loudly.
- **Type-hinted** — `from __future__ import annotations` at the top, fully annotated signatures.
- **Small** — if a tool grows past ~80 lines, consider splitting it.
