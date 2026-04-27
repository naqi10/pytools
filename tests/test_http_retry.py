from __future__ import annotations

import urllib.error
from typing import Any

import pytest

from pytools.web.http_retry import get


class _FakeResp:
    def __enter__(self) -> _FakeResp:
        return self

    def __exit__(self, *a: Any) -> None:
        pass

    def read(self) -> bytes:
        return b"ok"


def test_succeeds_first_try(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(_url: str, timeout: float) -> _FakeResp:
        return _FakeResp()

    monkeypatch.setattr("urllib.request.urlopen", fake)
    monkeypatch.setattr("time.sleep", lambda *_: None)
    assert get("http://x", retries=0, base=0) == b"ok"


def test_retries_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[int] = []

    def fake(_url: str, timeout: float) -> _FakeResp:
        calls.append(1)
        if len(calls) < 3:
            raise urllib.error.URLError("nope")
        return _FakeResp()

    monkeypatch.setattr("urllib.request.urlopen", fake)
    monkeypatch.setattr("time.sleep", lambda *_: None)
    assert get("http://x", retries=5, base=0) == b"ok"
    assert len(calls) == 3


def test_gives_up_after_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(_url: str, timeout: float) -> _FakeResp:
        raise urllib.error.URLError("nope")

    monkeypatch.setattr("urllib.request.urlopen", boom)
    monkeypatch.setattr("time.sleep", lambda *_: None)
    with pytest.raises(RuntimeError, match="failed after"):
        get("http://x", retries=2, base=0)
