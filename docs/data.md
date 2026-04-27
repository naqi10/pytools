# Data — data wrangling

## `pytools-json-repair`

Repair common LLM-broken JSON: stripped code fences (```` ```json ````), trailing commas, single-quoted keys and values.

```bash
cat broken.json | pytools-json-repair > fixed.json
```

```python
from pytools.data.json_repair import repair_json

repair_json("```json\n{'a': 1,}\n```")  # -> '{"a": 1}'
```

**Limitations:** does not handle single-quoted strings inside arrays (e.g. `['x', 'y']`) — only object keys and `key: 'value'` positions. Validates the result by parsing with `json.loads`; raises `JSONDecodeError` if still broken.

## `pytools-jq-lite`

Tiny jq-like dotted-path query for JSON. Supports `.key`, `[index]`, and `[]` (splat).

```bash
echo '{"a":{"b":[1,2,3]}}' | pytools-jq-lite .a.b[1]
# 2

cat data.json | pytools-jq-lite '.users[].name'
# "amy"
# "bob"
```

```python
from pytools.data.jq_lite import query

list(query({"users": [{"name": "amy"}, {"name": "bob"}]}, ".users[].name"))
# ["amy", "bob"]
```

For full jq syntax (filters, pipes, functions), use [`jq`](https://jqlang.github.io/jq/) itself — this is a 30-line approximation for the 80% case.

## `pytools-csv-to-jsonl`

Stream CSV to JSON Lines (one JSON object per row). Reads from stdin, writes to stdout — works with files of any size.

```bash
pytools-csv-to-jsonl < data.csv > data.jsonl
pytools-csv-to-jsonl --no-header --field-names a,b,c < data.csv
pytools-csv-to-jsonl --delimiter $'\t' < data.tsv
```

```python
import csv
from pytools.data.csv_to_jsonl import csv_to_jsonl

with open("data.csv") as f:
    for line in csv_to_jsonl(csv.reader(f)):
        print(line)
```

## `pytools-schema-diff`

Compare the inferred schemas of two JSON documents. Useful for catching API contract drift.

```bash
pytools-schema-diff old.json new.json
# + users[].verified: bool
# ~ users[].id: int -> string
```

```python
from pytools.data.schema_diff import schema, diff
import json

a = schema(json.loads(open("old.json").read()))
b = schema(json.loads(open("new.json").read()))
print(diff(a, b))
```

## `pytools-frequencies`

Count value frequencies at a JSON path across a JSONL stream. Pairs naturally with `pytools-jq-lite` syntax.

```bash
cat events.jsonl | pytools-frequencies .event_type
pytools-frequencies --top 10 .user.country < users.jsonl
```

```python
from pytools.data.frequencies import count

with open("events.jsonl") as f:
    counter = count(f, ".event_type")
print(counter.most_common(5))
```
