---
description: Stop the running Rojo sync server
allowed-tools: Bash
---

Stop any Rojo server started by this plugin.

Steps:
1. Find the Rojo process: `pgrep -f "rojo serve"`.
2. If nothing is running, say so and stop.
3. If a process is found, kill it with `kill <pid>`. Wait one second and verify it's gone with `pgrep -f "rojo serve"`. If still alive, use `kill -9 <pid>`.
4. Report which PID was stopped.
