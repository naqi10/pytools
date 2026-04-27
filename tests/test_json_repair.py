from __future__ import annotations

import json

import pytest

from pytools.data.json_repair import repair_json


def test_strips_code_fence() -> None:
    assert json.loads(repair_json('```json\n{"a": 1}\n```')) == {"a": 1}


def test_strips_bare_fence() -> None:
    assert json.loads(repair_json('```\n{"a": 1}\n```')) == {"a": 1}


def test_trailing_comma_object() -> None:
    assert json.loads(repair_json('{"a": 1,}')) == {"a": 1}


def test_trailing_comma_array() -> None:
    assert json.loads(repair_json('{"a": [1, 2, 3,]}')) == {"a": [1, 2, 3]}


def test_single_quoted_keys_and_values() -> None:
    assert json.loads(repair_json("{'name': 'amy'}")) == {"name": "amy"}


def test_combo() -> None:
    raw = "```\n{'items': [1,2,3,], 'ok': 'yes',}\n```"
    assert json.loads(repair_json(raw)) == {"items": [1, 2, 3], "ok": "yes"}


def test_already_valid_passthrough() -> None:
    assert json.loads(repair_json('{"a": 1, "b": [2, 3]}')) == {"a": 1, "b": [2, 3]}


def test_raises_on_unrepairable() -> None:
    with pytest.raises(json.JSONDecodeError):
        repair_json("not json at all {{{")
