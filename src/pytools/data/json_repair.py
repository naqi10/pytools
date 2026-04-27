"""Repair common LLM-broken JSON: code fences, trailing commas, single quotes.

CLI:
    cat broken.json | pytools-json-repair
    pytools-json-repair < broken.json > fixed.json

Library:
    from pytools.data.json_repair import repair_json
    repair_json("```json\\n{'a': 1,}\\n```")  # -> '{"a": 1}'

Limitations: does not handle single-quoted strings inside arrays
(e.g. `['x', 'y']`) — only object keys and `key: 'value'` positions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

_FENCE = re.compile(r"^\s*```(?:json)?\s*\n|\n\s*```\s*$", re.IGNORECASE | re.MULTILINE)
_TRAILING_COMMA = re.compile(r",(\s*[}\]])")
_SINGLE_QUOTED_KEY = re.compile(r"(?P<pre>[{,]\s*)'(?P<k>[^'\\]+)'(?P<post>\s*:)")
_SINGLE_QUOTED_VAL = re.compile(r"(?P<pre>:\s*)'(?P<v>[^'\\]*)'")


def repair_json(text: str) -> str:
    """Return repaired JSON text. Raises json.JSONDecodeError if still broken."""
    text = _FENCE.sub("", text).strip()
    text = _SINGLE_QUOTED_KEY.sub(r'\g<pre>"\g<k>"\g<post>', text)
    text = _SINGLE_QUOTED_VAL.sub(r'\g<pre>"\g<v>"', text)
    text = _TRAILING_COMMA.sub(r"\1", text)
    json.loads(text)
    return text


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(description="Repair LLM-broken JSON from stdin.").parse_args(argv)
    sys.stdout.write(repair_json(sys.stdin.read()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
