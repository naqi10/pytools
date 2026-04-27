from __future__ import annotations

import json

from pytools.data.csv_to_jsonl import csv_to_jsonl


def test_with_header_row() -> None:
    rows = [["name", "age"], ["amy", "30"], ["bob", "25"]]
    out = [json.loads(line) for line in csv_to_jsonl(rows)]
    assert out == [{"name": "amy", "age": "30"}, {"name": "bob", "age": "25"}]


def test_with_explicit_header() -> None:
    rows = [["amy", "30"], ["bob", "25"]]
    out = [json.loads(line) for line in csv_to_jsonl(rows, header=["name", "age"])]
    assert out == [{"name": "amy", "age": "30"}, {"name": "bob", "age": "25"}]


def test_empty_input_yields_nothing() -> None:
    assert list(csv_to_jsonl([["h1", "h2"]])) == []


def test_unicode_passthrough() -> None:
    rows = [["name"], ["café"]]
    out = list(csv_to_jsonl(rows))
    assert "café" in out[0]
