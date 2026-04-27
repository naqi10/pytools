from __future__ import annotations

from pytools.data.frequencies import count


def test_counts_simple_path() -> None:
    stream = [
        '{"event": "click"}',
        '{"event": "view"}',
        '{"event": "click"}',
    ]
    c = count(stream, ".event")
    assert c['"click"'] == 2
    assert c['"view"'] == 1


def test_skips_blank_lines() -> None:
    stream = ['{"a": 1}', "", "  ", '{"a": 1}']
    c = count(stream, ".a")
    assert c["1"] == 2


def test_skips_invalid_json() -> None:
    stream = ['{"a": 1}', "not json", '{"a": 2}']
    c = count(stream, ".a")
    assert sum(c.values()) == 2


def test_splat_path() -> None:
    stream = ['{"tags": ["x", "y"]}', '{"tags": ["x"]}']
    c = count(stream, ".tags[]")
    assert c['"x"'] == 2
    assert c['"y"'] == 1
