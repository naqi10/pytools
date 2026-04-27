from __future__ import annotations

import pytest

from pytools.web import sitemap_crawl


def test_yields_loc_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    body = b"""<?xml version='1.0'?>
    <urlset>
      <url><loc>https://example.com/a</loc></url>
      <url><loc>https://example.com/b</loc></url>
    </urlset>"""
    monkeypatch.setattr(sitemap_crawl, "get", lambda url, **_: body)
    assert list(sitemap_crawl.urls("https://example.com/sitemap.xml")) == [
        "https://example.com/a",
        "https://example.com/b",
    ]


def test_recursive_follows_sitemap_index(monkeypatch: pytest.MonkeyPatch) -> None:
    pages: dict[str, bytes] = {
        "https://x/index.xml": (
            b"<sitemapindex>"
            b"<sitemap><loc>https://x/a.xml</loc></sitemap>"
            b"<sitemap><loc>https://x/b.xml</loc></sitemap>"
            b"</sitemapindex>"
        ),
        "https://x/a.xml": b"<urlset><url><loc>https://x/page1</loc></url></urlset>",
        "https://x/b.xml": b"<urlset><url><loc>https://x/page2</loc></url></urlset>",
    }
    monkeypatch.setattr(sitemap_crawl, "get", lambda url, **_: pages[url])
    out = list(sitemap_crawl.urls("https://x/index.xml", recursive=True))
    assert out == ["https://x/page1", "https://x/page2"]


def test_non_recursive_does_not_follow(monkeypatch: pytest.MonkeyPatch) -> None:
    body = b"<sitemapindex><sitemap><loc>https://x/a.xml</loc></sitemap></sitemapindex>"
    monkeypatch.setattr(sitemap_crawl, "get", lambda url, **_: body)
    out = list(sitemap_crawl.urls("https://x/index.xml", recursive=False))
    assert out == ["https://x/a.xml"]
