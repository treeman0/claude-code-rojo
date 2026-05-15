---
description: Start the Rojo sync server in the background
allowed-tools: Bash
---

Start the Rojo server so changes sync to Roblox Studio.

Steps:
1. Check if a Rojo server is already running by looking for `rojo serve` in the process list. If one is running, report its PID and port and stop — do not start a second one.
2. Find the project file. Prefer `default.project.json` in the current working directory. If it does not exist, list any `*.project.json` files at the repo root and ask the user which one to use.
3. Start the server in the background, logging to `.rojo-server.log` in the working directory:
   ```
   nohup rojo serve <project-file> > .rojo-server.log 2>&1 &
   ```
4. Wait one second, then `tail -n 5 .rojo-server.log` to confirm it started cleanly (look for "Rojo server listening" or similar). If the log shows an error, report it.
5. Report the PID and the port (default 34872) so the user knows what's running.

Do not run this in the foreground — it must not block the session.
