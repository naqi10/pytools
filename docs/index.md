# pytools

> Tiny, professional Python tools. One file per problem. Stdlib-first.

`pytools` is a curated collection of single-file Python utilities — each small, type-hinted, tested, and cross-platform. Every tool is a library function **and** a CLI.

## Categories

- **[Dev](dev.md)** — developer productivity (`port-kill`, `git-churn`)
- **[Files](files.md)** — file wrangling (`dedupe`, `atomic-write`)
- **[Data](data.md)** — data wrangling (`json-repair`, `jq-lite`)
- **[Web](web.md)** — web/API (`http-retry`, `sse-parse`)

## Quick start

```bash
pip install -e ".[dev]"
pytools-json-repair < broken.json
echo '{"a":[1,2,3]}' | pytools-jq-lite '.a[]'
```

## Why pytools?

Inspired by [`Ten-lines-or-less`](https://github.com/cclauss/Ten-lines-or-less), rebuilt for the modern Python era:

| Axis | Original | pytools |
| --- | --- | --- |
| Platform | Pythonista (iOS) | Windows + macOS + Linux |
| Style | No types | Type-hinted, mypy-strict |
| Quality | Untested | Unit tests on every public function |
| Discovery | Alphabetical list | Categorised, tagged by problem |
| Dependencies | Mixed | Zero runtime deps |
