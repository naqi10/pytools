"""HTTP GET with exponential backoff and jitter — stdlib only.

CLI:
    pytools-http-retry https://example.com --retries 5

Library:
    from pytools.web.http_retry import get
    body = get("https://api.example.com/", retries=3, timeout=10)
"""

from __future__ import annotations

import argparse
import random
import sys
import time
import urllib.error
import urllib.request


def get(
    url: str,
    *,
    retries: int = 3,
    timeout: float = 10.0,
    base: float = 0.5,
) -> bytes:
    """GET `url`, retrying with exponential backoff. Returns response body."""
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read()  # type: ignore[no-any-return]
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            if attempt == retries:
                break
            time.sleep(base * (2**attempt) + random.uniform(0, base))
    raise RuntimeError(f"GET {url} failed after {retries + 1} attempts: {last}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="HTTP GET with retries and backoff.")
    p.add_argument("url")
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--timeout", type=float, default=10.0)
    args = p.parse_args(argv)

    sys.stdout.buffer.write(get(args.url, retries=args.retries, timeout=args.timeout))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
