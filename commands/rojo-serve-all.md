---
description: Start a Rojo sync server for EVERY *.project.json at the repo root, each on its own port
allowed-tools: Bash
---

Start one Rojo server per project file at the repo root so a multi-place project (e.g. a hub + a round place) can have Studio Connect into either side without port conflicts. Idempotent: any project that's already being served gets skipped, not duplicated.

Steps:

1. List all `*.project.json` files at the repo root via `ls *.project.json 2>/dev/null`. Sort alphabetically. If the list is empty, say "No `*.project.json` files at the repo root — nothing to serve" and stop. If the list has only one entry, suggest the user run `/rojo-serve` (single-server variant) instead, then continue and serve that one project.

2. Assign a port to each project file by index, starting at the Rojo default `34872` and incrementing. The alphabetically-first project gets `34872`, the second `34873`, etc. Display the planned mapping back to the user before starting anything:

   ```
   default.project.json → port 34872
   hub.project.json     → port 34873
   ```

3. Identify any servers already running by parsing `pgrep -af "rojo serve"` output. For each currently-running server, extract the project file name from the command line. Skip projects whose server is already running. If everything's already running, report the existing PIDs/ports and stop.

4. For each project that needs serving, start it in the background with its assigned port, logging to `.rojo-server-<basename>.log` where `<basename>` is the project file with `.project.json` stripped:

   ```
   nohup rojo serve <project-file> --port <port> > .rojo-server-<basename>.log 2>&1 &
   ```

   Use `run_in_background` on each Bash call so none of them block the session.

5. Wait two seconds, then tail each freshly-started log (`tail -n 5 .rojo-server-<basename>.log`) and verify it says "Rojo server listening". If any log shows an error (port already in use, bad project file, etc.), report which one failed and what it said.

6. Report the final state: for each running server, its PID, port, and the matching project file. Then tell the user how to connect from Studio: open each place, point the Rojo plugin at `localhost:<port>` matching the project that maps to it.

Do not run anything in the foreground. `/rojo-stop` continues to stop ALL Rojo servers (it matches on `rojo serve` regardless of project), so users can tear down everything with one command after starting multiples.
