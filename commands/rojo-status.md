---
description: Show whether the Rojo server is running and recent log output
allowed-tools: Bash
---

Report the current state of the Rojo server.

Steps:
1. Check for a running server: `pgrep -af "rojo serve"`. If none, say "No Rojo server running" and stop.
2. If running, report the PID and the command line.
3. If `.rojo-server.log` exists in the working directory, show its last 10 lines with `tail -n 10 .rojo-server.log`.
4. Confirm the default port is listening: `ss -ltn | grep 34872` (or `netstat -ltn | grep 34872` if `ss` is unavailable). Report whether the port is open.
