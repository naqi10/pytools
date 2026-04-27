from __future__ import annotations

from pytools.dev.env_lint import lint_env


def test_clean_file_has_no_issues() -> None:
    text = "# comment\nFOO=bar\nBAZ=qux\n"
    assert lint_env(text) == []


def test_detects_duplicate_keys() -> None:
    text = "FOO=1\nFOO=2\n"
    issues = lint_env(text)
    assert len(issues) == 1
    assert "duplicate" in issues[0][1]


def test_detects_missing_equals() -> None:
    text = "FOO_NO_EQUALS\n"
    issues = lint_env(text)
    assert issues[0][0] == 1
    assert "missing '='" in issues[0][1]


def test_detects_empty_value() -> None:
    text = "FOO=\n"
    issues = lint_env(text)
    assert any("empty value" in msg for _, msg in issues)


def test_detects_unquoted_space() -> None:
    text = "FOO=hello world\n"
    issues = lint_env(text)
    assert any("unquoted space" in msg for _, msg in issues)


def test_quoted_space_ok() -> None:
    text = 'FOO="hello world"\n'
    assert lint_env(text) == []


def test_skips_blank_and_comment_lines() -> None:
    text = "\n# top comment\n\nFOO=bar\n"
    assert lint_env(text) == []
