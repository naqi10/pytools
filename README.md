# pytools

> Tiny, professional Python tools. One file per problem. Stdlib-first.

`pytools` is a curated collection of single-file Python utilities — each is small, type-hinted, tested, and runnable on Windows, macOS, and Linux. Inspired by the spirit of [`Ten-lines-or-less`](https://github.com/cclauss/Ten-lines-or-less), but rebuilt for the modern Python era: no platform-specific dependencies, every script ships as both a library function and a CLI, every script has tests.

## Install (local, editable)

```bash
pip install -e ".[dev]"
```

This project is intentionally **not published** to PyPI. It's installed locally from this checkout.

## Tools

### dev — developer productivity

| Command | What it does |
| --- | --- |
| `pytools-port-kill PORT [--dry-run]` | Kill the process listening on a TCP port. |
| `pytools-git-churn [--since 30.days] [--top 10]` | Top files by lines added + removed in a git repo. |
| `pytools-dead-imports PATH` | Find unused imports via AST (heuristic). |
| `pytools-env-lint .env` | Validate a `.env` file: duplicates, empty values, unquoted spaces. |
| `pytools-todo-grep [PATH] [--tags TODO,XXX]` | Find TODO/FIXME/XXX/HACK markers, grouped by tag. |

### files — file wrangling

| Command | What it does |
| --- | --- |
| `pytools-dedupe DIR [--min-size N]` | Find duplicate files by SHA-256, grouped. |
| `pytools-atomic-write FILE` | Pipe stdin into FILE atomically (temp → fsync → rename). |
| `pytools-find-content PATTERN [DIR]` | Recursive grep, binary-skipping. |
| `pytools-normalize-eol DIR --to lf` | Normalize line endings (LF/CRLF/CR) under a tree. |
| `pytools-safe-rename PATTERN REPL [DIR]` | Bulk regex rename with collision check + undo log. |

### data — data wrangling

| Command | What it does |
| --- | --- |
| `pytools-json-repair < broken.json` | Fix LLM-broken JSON: code fences, trailing commas, single quotes. |
| `pytools-jq-lite '.users[].name' < data.json` | Tiny jq-like dotted-path query. |
| `pytools-csv-to-jsonl < data.csv` | Stream CSV to JSON Lines. |
| `pytools-schema-diff old.json new.json` | Diff inferred schemas of two JSON documents. |
| `pytools-frequencies .field < data.jsonl` | Count value frequencies at a JSON path across a JSONL stream. |

### web — web/API

| Command | What it does |
| --- | --- |
| `pytools-http-retry URL [--retries N]` | HTTP GET with exponential backoff + jitter. |
| `pytools-sse-parse [URL]` | Parse a Server-Sent Events stream into JSON-per-line. |
| `pytools-sitemap-crawl URL [--recursive]` | Fetch a sitemap.xml and yield its URLs. |
| `pytools-headers-check URL` | Report presence of common security headers. |
| `pytools-url-status < urls.txt` | HEAD-check URLs from stdin; report status codes. |

## Use as a library

Every CLI has a clean importable function:

```python
from pytools.data.json_repair import repair_json
from pytools.files.atomic_write import atomic_write
from pytools.web.http_retry import get

repair_json("```json\n{'a': 1,}\n```")  # -> '{"a": 1}'

with atomic_write("out.json") as f:
    f.write('{"ok": true}')

body = get("https://example.com/", retries=3, timeout=10)
```

## Project layout

```
src/pytools/
├── dev/         developer productivity tools
├── files/       filesystem tools
├── data/        data wrangling tools
└── web/         web/API tools
tests/           one test file per tool
```

## Design rules

Every tool follows the same shape so they're easy to read, copy, and extend:

1. **One file, one purpose** — under `src/pytools/<category>/<name>.py`.
2. **Stdlib first** — runtime dependencies require justification; right now there are zero.
3. **Library + CLI** — every tool exposes a callable function and an `argparse` `main()`.
4. **Type-hinted, ruff-clean, mypy-strict** — enforced by CI on Python 3.10–3.13.
5. **Tested** — every public function has unit tests in `tests/`.

## Develop

```bash
pip install -e ".[dev]"
pytest                # run tests
ruff check .          # lint
ruff format .         # format
mypy                  # type-check
```

## Adding a new tool

1. Create `src/pytools/<category>/<your_tool>.py` with a module docstring, a callable function, and an `argparse` `main()`.
2. Create `tests/test_<your_tool>.py` covering the function (not the CLI).
3. Add a `pytools-<your-tool>` entry to `[project.scripts]` in `pyproject.toml`.
4. Add a row to the table in this README.
5. `pytest && ruff check . && mypy`.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Ali Naqi.
