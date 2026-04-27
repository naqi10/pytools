"""Kill the process listening on a TCP port. Cross-platform, stdlib-only.

Examples:
    pytools-port-kill 3000
    pytools-port-kill 8080 --dry-run

Library:
    from pytools.dev.port_kill import find_pids, kill
    for pid in find_pids(3000):
        kill(pid)
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import subprocess
import sys


def find_pids(port: int) -> list[int]:
    """Return PIDs of processes listening on `port`."""
    if platform.system() == "Windows":
        out = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        pat = re.compile(rf":{port}\s+\S+\s+LISTENING\s+(\d+)")
        return sorted({int(m.group(1)) for m in pat.finditer(out)})
    out = subprocess.run(
        ["lsof", f"-tiTCP:{port}", "-sTCP:LISTEN"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    return [int(x) for x in out.split() if x.isdigit()]


def kill(pid: int) -> None:
    """Force-terminate a process by PID."""
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
    else:
        os.kill(pid, 9)  # SIGKILL on POSIX; not available as a symbol on Windows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Kill the process listening on a TCP port.")
    p.add_argument("port", type=int)
    p.add_argument("--dry-run", action="store_true", help="show PIDs without killing")
    args = p.parse_args(argv)

    pids = find_pids(args.port)
    if not pids:
        print(f"nothing listening on :{args.port}", file=sys.stderr)
        return 1
    for pid in pids:
        if args.dry_run:
            print(f"would kill {pid}")
        else:
            kill(pid)
            print(f"killed {pid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
