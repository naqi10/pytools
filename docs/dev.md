# Dev — developer productivity

## `pytools-port-kill`

Kill the process listening on a TCP port. Cross-platform (uses `netstat`/`taskkill` on Windows, `lsof`/`SIGKILL` on Unix).

```bash
pytools-port-kill 3000
pytools-port-kill 8080 --dry-run
```

```python
from pytools.dev.port_kill import find_pids, kill

for pid in find_pids(3000):
    kill(pid)
```

## `pytools-git-churn`

Top N files by lines added + removed in a git repo. Useful for finding hot spots and refactor targets.

```bash
pytools-git-churn --since 30.days --top 10
pytools-git-churn --since 2024-01-01 --repo /path/to/repo
```

```python
from pytools.dev.git_churn import churn

totals = churn("30.days", repo=".")
# {"src/foo.py": 423, "src/bar.py": 219, ...}
```

## `pytools-dead-imports`

Heuristic AST-based finder of unused imports. For canonical results, use ruff's F401 — this is a tiny educational version that handles the common cases.

```bash
pytools-dead-imports src/
pytools-dead-imports myfile.py
```

```python
from pytools.dev.dead_imports import dead_imports

dead_imports("import os\nimport sys\nprint(sys.argv)\n")
# [(1, "os")]
```

**Limitations:** does not catch dynamic uses (`getattr`), `__all__` re-exports, or string annotations under `from __future__ import annotations`.

## `pytools-env-lint`

Validate a `.env` file. Catches duplicate keys, missing `=`, empty values, and unquoted spaces in values.

```bash
pytools-env-lint .env
pytools-env-lint .env.production
```

```python
from pytools.dev.env_lint import lint_env

lint_env("FOO=1\nFOO=2\n")
# [(2, "duplicate key 'FOO' (first defined on line 1)")]
```

## `pytools-todo-grep`

Find TODO/FIXME/XXX/HACK markers across a tree. Groups results by tag for a clean overview.

```bash
pytools-todo-grep src/
pytools-todo-grep --tags TODO,REVIEW .
```

```python
from pytools.dev.todo_grep import find_todos
from pathlib import Path

found = find_todos(Path("src"))
for tag, items in found.items():
    print(tag, len(items))
```
