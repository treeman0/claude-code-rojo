#!/bin/bash
# Pre-edit hook: if we're in a Rojo project but the server isn't running,
# print a non-blocking notice to stderr. Exit 0 so the edit still proceeds.

if ls *.project.json >/dev/null 2>&1; then
  if ! pgrep -f "rojo serve" >/dev/null 2>&1; then
    echo "[rojo-helper] Heads up: editing a Rojo project but no rojo server is running. Use /rojo-serve to start syncing." >&2
  fi
fi

exit 0
