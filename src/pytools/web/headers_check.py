"""Check security-relevant HTTP response headers for a URL.

Examples:
    pytools-headers-check https://example.com

Reports presence of common hardening headers: HSTS, CSP, X-Frame-Options,
X-Content-Type-Options, Referrer-Policy, Permissions-Policy.
"""

from __future__ import annotations

import argparse
import urllib.request

CHECKS: tuple[str, ...] = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
)


def check(url: str, *, timeout: float = 10.0) -> dict[str, str | None]:
    """Return {header_name: value_or_None} for the headers in CHECKS."""
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return {name: r.headers.get(name) for name in CHECKS}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Check security headers on a URL.")
    p.add_argument("url")
    p.add_argument("--timeout", type=float, default=10.0)
    args = p.parse_args(argv)

    results = check(args.url, timeout=args.timeout)
    missing = 0
    for name, value in results.items():
        mark = "OK" if value else "--"
        print(f"  [{mark}] {name}: {value or '(missing)'}")
        if value is None:
            missing += 1
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
