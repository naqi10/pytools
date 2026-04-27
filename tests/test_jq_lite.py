from __future__ import annotations

from pytools.data.jq_lite import query


def test_root_dot() -> None:
    assert list(query({"a": 1}, ".")) == [{"a": 1}]


def test_empty_path_yields_root() -> None:
    assert list(query([1, 2], "")) == [[1, 2]]


def test_nested_dotted_keys() -> None:
    assert list(query({"a": {"b": {"c": 42}}}, ".a.b.c")) == [42]


def test_array_index() -> None:
    assert list(query({"a": [10, 20, 30]}, ".a[1]")) == [20]


def test_splat_yields_each_element() -> None:
    data = {"users": [{"name": "amy"}, {"name": "bob"}]}
    assert list(query(data, ".users[].name")) == ["amy", "bob"]


def test_splat_at_root() -> None:
    assert list(query([1, 2, 3], ".[]")) == [1, 2, 3]


def test_keys_with_underscores_and_hyphens() -> None:
    assert list(query({"a_b-c": 1}, ".a_b-c")) == [1]
