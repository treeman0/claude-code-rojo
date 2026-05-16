#!/usr/bin/env python3
"""
Pre-edit hook for rojo-helper: if we're in a Rojo project but the server
isn't running, print a non-blocking notice to stderr.

Always exits 0 — the edit always proceeds. The notice is informational.

Cross-platform: works on macOS, Linux, and Windows (including Git Bash / MSYS
and native Python on Windows).
"""
import glob
import os
import sys


def rojo_server_running() -> bool:
    """Best-effort check for a running 'rojo serve' process.

    On Unix-like systems with pgrep, use it. On Windows, use tasklist with a
    /v filter. If neither works, return False (we just won't show the notice
    when we should — better than a crash)."""
    try:
        import subprocess
        if os.name == "nt":
            # tasklist /v shows window titles + command lines.
            res = subprocess.run(
                ["tasklist", "/v", "/fo", "csv"],
                capture_output=True, text=True, timeout=3,
            )
            return res.returncode == 0 and "rojo" in (res.stdout or "").lower() \
                and "serve" in (res.stdout or "").lower()
        # POSIX
        res = subprocess.run(
            ["pgrep", "-f", "rojo serve"],
            capture_output=True, timeout=3,
        )
        return res.returncode == 0
    except Exception:
        return False


def main():
    # Only warn if there's a *.project.json file in the CWD
    if not glob.glob("*.project.json"):
        sys.exit(0)
    if rojo_server_running():
        sys.exit(0)
    print(
        "[rojo-helper] Heads up: editing a Rojo project but no rojo server "
        "is running. Use /rojo-serve to start syncing.",
        file=sys.stderr,
    )
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Never let this hook crash and block an edit.
        sys.exit(0)
