"""Bulk HEAD-check URLs from stdin; report status code and final URL.

Examples:
    cat urls.txt | pytools-url-status
    pytools-sitemap-crawl https://x.com/sitemap.xml | pytools-url-status
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request


def status(url: str, *, timeout: float = 10.0) -> tuple[int, str]:
    """Return (status_code, final_url). Status -1 on connection error."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except (urllib.error.URLError, TimeoutError, ValueError):
        return -1, url


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="HEAD-check URLs from stdin.")
    p.add_argument("--timeout", type=float, default=10.0)
    args = p.parse_args(argv)

    failed = 0
    for raw in sys.stdin:
        url = raw.strip()
        if not url:
            continue
        code, final = status(url, timeout=args.timeout)
        if code >= 400 or code < 0:
            failed += 1
        suffix = f" -> {final}" if final != url else ""
        print(f"{code:>4}  {url}{suffix}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
