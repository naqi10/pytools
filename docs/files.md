# Files — file wrangling

## `pytools-dedupe`

Find duplicate files under a directory by SHA-256 hash. Skips files smaller than `--min-size`. First groups by file size to avoid hashing unique files.

```bash
pytools-dedupe ~/Downloads
pytools-dedupe . --min-size 1024
```

```python
from pytools.files.dedupe import find_duplicates
from pathlib import Path

dupes = find_duplicates(Path("."), min_size=1024)
for digest, paths in dupes.items():
    print(digest, paths)
```

## `pytools-atomic-write`

Atomic file writes — write to a temp file, fsync, then rename. The target file is either fully updated or untouched; partial writes are impossible.

```bash
echo hello | pytools-atomic-write out.txt
```

```python
from pytools.files.atomic_write import atomic_write

with atomic_write("config.json") as f:
    f.write('{"version": 2}')

# On error inside the block, the temp file is removed and config.json is unchanged.
```

## `pytools-find-content`

Recursive grep that skips binary files (heuristic: null byte in first 8 KB) and decodes as UTF-8.

```bash
pytools-find-content "TODO" src/
pytools-find-content --regex "def\\s+main" .
pytools-find-content -i "error" logs/
```

```python
import re
from pathlib import Path
from pytools.files.find_by_content import search

for path, line, content in search(Path("src"), re.compile(r"^class\s+\w+")):
    print(path, line, content)
```

## `pytools-normalize-eol`

Normalize text-file line endings to `lf`, `crlf`, or `cr`. Skips binaries; idempotent.

```bash
pytools-normalize-eol --to lf src/
pytools-normalize-eol --to crlf --dry-run docs/
```

```python
from pathlib import Path
from pytools.files.normalize_eol import normalize

normalize(Path("script.sh"), b"\n")  # True if changed
```

## `pytools-safe-rename`

Bulk regex rename. Refuses to apply if two source paths target the same name, or if a rename would overwrite an existing file. Writes an undo log.

```bash
pytools-safe-rename '\.txt$' '.md' src/
pytools-safe-rename --dry-run '^old_' 'new_' .
pytools-safe-rename --undo .pytools-rename.log
```

```python
import re
from pathlib import Path
from pytools.files.safe_rename import plan, apply, undo

pairs = plan(Path("."), re.compile(r"\.txt$"), ".md")
apply(pairs, Path(".pytools-rename.log"))
# later:
undo(Path(".pytools-rename.log"))
```
