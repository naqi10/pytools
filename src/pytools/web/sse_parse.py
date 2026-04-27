"""Parse a Server-Sent Events (SSE) stream into JSON-per-line.

CLI:
    pytools-sse-parse https://example.com/events
    cat stream.txt | pytools-sse-parse

Library:
    from pytools.web.sse_parse import iter_events
    for ev in iter_events(line_iterator):
        print(ev.get("event"), ev.get("data"))
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from collections.abc import Iterable, Iterator


def iter_events(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Yield event dicts as defined by the SSE spec.

    Multi-value fields (typically `data:`) are joined with newlines.
    Comment lines (`:foo`) and unknown fields are handled per spec.
    """
    event: dict[str, list[str]] = {}
    for raw in lines:
        line = raw.rstrip("\r\n")
        if not line:
            if event:
                yield {k: "\n".join(v) for k, v in event.items()}
                event = {}
            continue
        if line.startswith(":"):
            continue
        field, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        event.setdefault(field, []).append(value)
    if event:
        yield {k: "\n".join(v) for k, v in event.items()}


def _from_url(url: str) -> Iterator[str]:
    req = urllib.request.Request(url, headers={"Accept": "text/event-stream"})
    with urllib.request.urlopen(req) as r:
        for line in r:
            yield line.decode("utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Parse Server-Sent Events into JSON-per-line.")
    p.add_argument("url", nargs="?", help="if omitted, read SSE stream from stdin")
    args = p.parse_args(argv)

    src: Iterable[str] = _from_url(args.url) if args.url else sys.stdin
    for ev in iter_events(src):
        print(json.dumps(ev, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
