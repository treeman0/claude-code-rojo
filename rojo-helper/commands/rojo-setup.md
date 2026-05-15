---
description: Install or update Rojo dependencies to the pinned stable versions
allowed-tools: Bash
---

Bring the Rojo toolchain to the pinned stable versions. This command makes changes to the user's system, so it must confirm before each step that installs or modifies anything.

**Pinned versions:**
- Rojo CLI: **7.6.1** (latest stable)
- Rokit: latest stable from upstream

**Steps:**

1. **Run the equivalent of `/rojo-doctor` first.** Gather the same diagnostic info: platform, Rokit version, Rojo version, `rokit.toml` state, Studio installed?, Studio plugin present?. Print the summary so the user can see what's about to change. Do not skip this — the user needs to see the current state before agreeing to changes.

2. **Ask for confirmation before proceeding.** Print: "About to make the following changes: ... Proceed? (y/n)" and wait for the user. If they say no, stop.

3. **Install Rokit if missing.**
   - On macOS/Linux: instruct the user to run, in a separate terminal (do not pipe to bash automatically):
     ```
     curl -sSf https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | bash
     ```
   - On Windows PowerShell:
     ```
     Invoke-RestMethod https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.ps1 | Invoke-Expression
     ```
   - After they confirm they've run it, instruct them to open a new shell (so PATH is reloaded) and re-run `/rojo-setup`. Stop here on this run.
   - Do NOT silently pipe shell installers from inside the slash command. Always show the command, get explicit user confirmation, and let them run it themselves.

4. **Update Rokit if outdated.**
   - Run `rokit self-update` (this is the official self-update path; if the user's Rokit is old enough that this subcommand doesn't exist, fall back to re-running the install script as in step 3).
   - Verify with `rokit --version` after.

5. **Set up `rokit.toml` in the working directory if missing.**
   - If no `rokit.toml`, run `rokit init`.
   - Run `rokit add rojo-rbx/rojo@7.6.1`. If it's already pinned to 7.6.1, skip.
   - If `rokit.toml` exists and pins a different version, ASK the user: "Project currently pins Rojo X.Y.Z; change to 7.6.1? (y/n)". Only change it if they agree.
   - Run `rokit install` to download/build the pinned tool.

6. **Verify Rojo CLI.**
   - Run `rojo --version`. Confirm it reports `Rojo 7.6.1`. If not, surface the mismatch (most likely PATH issue: an older `rojo` is still being resolved first; tell the user to check `which rojo` / `where rojo` against `~/.rokit/bin`).

7. **Check Roblox Studio.**
   - If not detected, tell the user to install it from https://www.roblox.com/create (the Studio installer requires a Roblox account login, so this MUST be a manual step — do not try to script it).
   - If detected, continue.

8. **Install/update the Studio plugin.**
   - Run `rojo plugin install`. This drops `RojoManagedPlugin.rbxm` into Studio's plugins folder using the CLI's bundled plugin, so versions match by construction.
   - Tell the user to restart Roblox Studio. If they previously installed the Rojo plugin from the Roblox marketplace, tell them to disable it in Studio's plugin manager so the two don't conflict.

9. **Final verification.**
   - Re-run the diagnostic from step 1. Print the new state. Confirm "All good" if every check passes. Otherwise list remaining issues.

**Important behaviors:**
- This command is idempotent. Re-running it on a healthy system should be a no-op (every step short-circuits).
- Never use `sudo` or admin elevation. If something would require it, fail and tell the user to do it themselves.
- Never download or execute binaries from sources other than the official upstream URLs listed in step 3.
- If any step fails, stop and report the error verbatim. Do not silently continue.
