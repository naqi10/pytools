from __future__ import annotations

import urllib.error
from typing import Any

import pytest

from pytools.web.url_status import status


class _FakeResp:
    def __init__(self, code: int, final: str) -> None:
        self.status = code
        self._final = final

    def __enter__(self) -> _FakeResp:
        return self

    def __exit__(self, *a: Any) -> None:
        pass

    def geturl(self) -> str:
        return self._final


def test_ok_status(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(req: Any, timeout: float) -> _FakeResp:
        return _FakeResp(200, "https://example.com/")

    monkeypatch.setattr("urllib.request.urlopen", fake)
    assert status("https://example.com/") == (200, "https://example.com/")


def test_http_error_returns_status_code(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(req: Any, timeout: float) -> _FakeResp:
        raise urllib.error.HTTPError("http://x", 404, "Not Found", {}, None)  # type: ignore[arg-type]

    monkeypatch.setattr("urllib.request.urlopen", fake)
    code, _ = status("http://x")
    assert code == 404


def test_connection_error_returns_negative(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(req: Any, timeout: float) -> _FakeResp:
        raise urllib.error.URLError("nope")

    monkeypatch.setattr("urllib.request.urlopen", fake)
    code, _ = status("http://x")
    assert code == -1


def test_redirect_reports_final_url(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(req: Any, timeout: float) -> _FakeResp:
        return _FakeResp(200, "https://example.com/final")

    monkeypatch.setattr("urllib.request.urlopen", fake)
    code, final = status("https://example.com/start")
    assert code == 200
    assert final == "https://example.com/final"
