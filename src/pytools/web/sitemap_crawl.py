"""Fetch a sitemap.xml and yield its URLs (handles sitemap indexes).

Examples:
    pytools-sitemap-crawl https://example.com/sitemap.xml
    pytools-sitemap-crawl --recursive https://example.com/sitemap_index.xml
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterator

from pytools.web.http_retry import get

_LOC = re.compile(r"<loc>([^<]+)</loc>", re.IGNORECASE)
_SITEMAP_BLOCK = re.compile(r"<sitemap>(.*?)</sitemap>", re.IGNORECASE | re.DOTALL)


def urls(sitemap_url: str, *, recursive: bool = False) -> Iterator[str]:
    """Yield <loc> URLs from a sitemap. With recursive=True, follow sitemap indexes."""
    body = get(sitemap_url, retries=3, timeout=15).decode("utf-8", errors="replace")
    if recursive and _SITEMAP_BLOCK.search(body):
        for block in _SITEMAP_BLOCK.findall(body):
            for sub in _LOC.findall(block):
                yield from urls(sub, recursive=True)
        return
    yield from _LOC.findall(body)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Fetch sitemap URLs.")
    p.add_argument("url")
    p.add_argument("--recursive", action="store_true", help="follow sitemap-index entries")
    args = p.parse_args(argv)

    for u in urls(args.url, recursive=args.recursive):
        print(u)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
