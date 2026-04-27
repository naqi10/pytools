from __future__ import annotations

from typing import Any

import pytest

from pytools.web.headers_check import CHECKS, check


class _FakeHeaders:
    def __init__(self, data: dict[str, str]) -> None:
        self._data = data

    def get(self, key: str) -> str | None:
        return self._data.get(key)


class _FakeResp:
    def __init__(self, headers: dict[str, str]) -> None:
        self.headers = _FakeHeaders(headers)

    def __enter__(self) -> _FakeResp:
        return self

    def __exit__(self, *a: Any) -> None:
        pass


def test_returns_all_check_names(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(req: Any, timeout: float) -> _FakeResp:
        return _FakeResp({"Strict-Transport-Security": "max-age=31536000"})

    monkeypatch.setattr("urllib.request.urlopen", fake)
    result = check("https://example.com")
    assert set(result) == set(CHECKS)
    assert result["Strict-Transport-Security"] == "max-age=31536000"
    assert result["Content-Security-Policy"] is None


def test_all_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(req: Any, timeout: float) -> _FakeResp:
        return _FakeResp({})

    monkeypatch.setattr("urllib.request.urlopen", fake)
    result = check("https://example.com")
    assert all(v is None for v in result.values())
