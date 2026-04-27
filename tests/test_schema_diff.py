from __future__ import annotations

from pytools.data.schema_diff import diff, schema


def test_schema_basic_object() -> None:
    s = schema({"name": "x", "age": 30})
    assert s == {".": "object", "name": "string", "age": "int"}


def test_schema_nested() -> None:
    s = schema({"a": {"b": [1, 2]}})
    assert s["a"] == "object"
    assert s["a.b"] == "array"
    assert s["a.b[]"] == "int"


def test_diff_added_and_removed() -> None:
    old = schema({"a": 1})
    new = schema({"a": 1, "b": "hi"})
    out = diff(old, new)
    assert any(line.startswith("+ b") for line in out)


def test_diff_type_change() -> None:
    old = schema({"a": 1})
    new = schema({"a": "now string"})
    out = diff(old, new)
    assert any(line.startswith("~ a") and "int -> string" in line for line in out)


def test_no_diff_for_identical() -> None:
    a = schema({"x": [1, 2, 3]})
    b = schema({"x": [4, 5, 6]})
    assert diff(a, b) == []
