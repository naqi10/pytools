from __future__ import annotations

from pytools.web.sse_parse import iter_events


def test_basic_event() -> None:
    stream = ["event: ping\n", "data: hello\n", "\n"]
    assert list(iter_events(stream)) == [{"event": "ping", "data": "hello"}]


def test_multiline_data_joined() -> None:
    stream = ["data: line1\n", "data: line2\n", "\n"]
    assert list(iter_events(stream)) == [{"data": "line1\nline2"}]


def test_skips_comments() -> None:
    stream = [": this is a comment\n", "data: x\n", "\n"]
    assert list(iter_events(stream)) == [{"data": "x"}]


def test_multiple_events() -> None:
    stream = ["data: a\n", "\n", "data: b\n", "\n"]
    assert list(iter_events(stream)) == [{"data": "a"}, {"data": "b"}]


def test_single_leading_space_stripped() -> None:
    stream = ["data:  hello\n", "\n"]
    assert list(iter_events(stream)) == [{"data": " hello"}]


def test_trailing_event_without_blank_line() -> None:
    stream = ["data: tail\n"]
    assert list(iter_events(stream)) == [{"data": "tail"}]


def test_handles_crlf() -> None:
    stream = ["data: x\r\n", "\r\n"]
    assert list(iter_events(stream)) == [{"data": "x"}]
