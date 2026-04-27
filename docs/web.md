# Web — web and API

## `pytools-http-retry`

HTTP GET with exponential backoff and jitter. Stdlib-only — no `requests` dependency.

```bash
pytools-http-retry https://example.com --retries 5 --timeout 10
```

```python
from pytools.web.http_retry import get

body = get("https://api.example.com/data", retries=3, timeout=10)
```

Backoff schedule: `base * 2^attempt + uniform(0, base)` seconds, where `base` defaults to 0.5s.

## `pytools-sse-parse`

Parse a Server-Sent Events (SSE) stream into JSON-per-line. Reads from a URL or stdin.

```bash
pytools-sse-parse https://example.com/events
cat captured-stream.txt | pytools-sse-parse
```

```python
from pytools.web.sse_parse import iter_events

with open("stream.txt") as f:
    for ev in iter_events(f):
        print(ev.get("event"), ev.get("data"))
```

Spec-compliant: comments (`:foo`) are skipped, multi-value fields (typically `data:`) are joined with newlines, single leading space after `:` is stripped.

## `pytools-sitemap-crawl`

Fetch a `sitemap.xml` and yield its URLs. With `--recursive`, follow `<sitemap>` entries inside a sitemap index.

```bash
pytools-sitemap-crawl https://example.com/sitemap.xml
pytools-sitemap-crawl --recursive https://example.com/sitemap_index.xml
```

```python
from pytools.web.sitemap_crawl import urls

for u in urls("https://example.com/sitemap.xml", recursive=True):
    print(u)
```

## `pytools-headers-check`

Report presence of common HTTP security/hardening headers. Returns exit code 1 if any header is missing.

```bash
pytools-headers-check https://example.com
#   [OK] Strict-Transport-Security: max-age=31536000
#   [--] Content-Security-Policy: (missing)
#   ...
```

```python
from pytools.web.headers_check import check

check("https://example.com")
# {"Strict-Transport-Security": "max-age=...", "Content-Security-Policy": None, ...}
```

## `pytools-url-status`

Bulk HEAD-check URLs from stdin. Reports status code, follows redirects, and shows the final URL when it differs.

```bash
cat urls.txt | pytools-url-status
pytools-sitemap-crawl https://x.com/sitemap.xml | pytools-url-status
```

```python
from pytools.web.url_status import status

code, final = status("https://example.com/")  # (200, "https://example.com/")
```

Status `-1` indicates a connection error (DNS failure, timeout, refused).
