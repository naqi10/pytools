"""Atomic file writes — write to temp, fsync, rename. Crash-safe.

CLI (writes stdin to PATH atomically):
    echo hello | pytools-atomic-write out.txt

Library:
    from pytools.files.atomic_write import atomic_write
    with atomic_write("out.json") as f:
        f.write('{"ok": true}')
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import IO, Any


@contextmanager
def atomic_write(
    path: str | os.PathLike[str],
    mode: str = "w",
    **kwargs: Any,
) -> Iterator[IO[Any]]:
    """Yield a writable file handle whose contents are committed atomically.

    On success: temp file is fsync'd and renamed over `path`.
    On exception: temp file is removed; the original `path` is untouched.
    """
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    os.close(fd)
    tmp_path = Path(tmp)
    try:
        with tmp_path.open(mode, **kwargs) as f:
            yield f
            f.flush()
            os.fsync(f.fileno())
        tmp_path.replace(path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Pipe stdin into PATH atomically.")
    p.add_argument("path", type=Path)
    args = p.parse_args(argv)

    data = sys.stdin.buffer.read()
    with atomic_write(args.path, "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
