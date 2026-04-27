"""Stream CSV to JSON Lines (one JSON object per row).

Examples:
    pytools-csv-to-jsonl < data.csv > data.jsonl
    pytools-csv-to-jsonl --no-header --field-names a,b,c < data.csv
    pytools-csv-to-jsonl --delimiter '\\t' < data.tsv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections.abc import Iterable, Iterator


def csv_to_jsonl(rows: Iterable[list[str]], header: list[str] | None = None) -> Iterator[str]:
    """Yield JSON-serialized dicts. If `header` is None, the first row is used."""
    iterator = iter(rows)
    if header is None:
        header = next(iterator)
    for row in iterator:
        yield json.dumps(dict(zip(header, row, strict=False)), ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Stream CSV from stdin to JSON Lines on stdout.")
    p.add_argument("--no-header", action="store_true")
    p.add_argument("--field-names", help="comma-separated names (required with --no-header)")
    p.add_argument("--delimiter", default=",")
    args = p.parse_args(argv)

    if args.no_header and not args.field_names:
        print("error: --no-header requires --field-names", file=sys.stderr)
        return 2

    reader = csv.reader(sys.stdin, delimiter=args.delimiter)
    header = args.field_names.split(",") if args.no_header else None
    for line in csv_to_jsonl(reader, header):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
