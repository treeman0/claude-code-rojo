---
description: Check that all Rojo dependencies are installed and up to date (read-only)
allowed-tools: Bash
---

Run a read-only health check on the Rojo toolchain. Make NO changes — only report.

**Pinned versions (compare against these):**
- Rojo CLI: **7.6.1** (current stable)
- Rokit: latest stable

**Steps:**

1. **Detect platform.** Run `uname -s` and capture the result. Branch:
   - `Linux` or `Darwin` → Unix-style checks.
   - `MINGW*`, `MSYS*`, `CYGWIN*` → Git Bash on Windows.
   - If `uname` is missing entirely, assume native Windows (PowerShell/cmd) and adjust commands.

2. **Check Rokit.**
   - Run `rokit --version`. If the binary is missing, mark Rokit as MISSING.
   - If present, fetch the latest release tag from `https://api.github.com/repos/rojo-rbx/rokit/releases/latest` (use `curl -s` on Unix, `Invoke-RestMethod` on Windows). Compare to installed version. Mark UP TO DATE or OUTDATED.
   - On failure to reach GitHub, mark as UNKNOWN and note the network issue.

3. **Check Rojo CLI.**
   - Run `rojo --version`. If missing, mark MISSING.
   - Parse the version. Compare to **7.6.1**.
     - Exact match → UP TO DATE (pinned).
     - Lower than 7.6.1 → OUTDATED.
     - Higher than 7.6.1 (e.g., 7.7.0-rc.1) → NEWER THAN PINNED (note: user is ahead of pin; not an error, but call it out).

4. **Check `rokit.toml` in the working directory.**
   - If it exists, read it and report which version of `rojo-rbx/rojo` is pinned.
   - If it pins a version other than 7.6.1, flag MISMATCH between project pin and plugin pin.
   - If no `rokit.toml`, mark as MISSING PROJECT PIN (recommend `/rojo-setup` to create one).

5. **Check Roblox Studio installation.**
   - Look for the Studio executable in the standard locations:
     - macOS: `/Applications/RobloxStudio.app`
     - Windows: `%LOCALAPPDATA%\Roblox\Versions\` (any `RobloxStudioBeta.exe` inside)
     - Linux: Roblox Studio is not officially supported; mark UNSUPPORTED PLATFORM.
   - If found, mark INSTALLED. If not, mark MISSING.

6. **Check the Studio plugin file.**
   - Look for `RojoManagedPlugin.rbxm` in Studio's plugins folder:
     - macOS: `~/Documents/Roblox/Plugins/RojoManagedPlugin.rbxm`
     - Windows: `%LOCALAPPDATA%\Roblox\Plugins\RojoManagedPlugin.rbxm`
   - If present, mark INSTALLED. We can't easily read its version from the binary, so don't try — just note that `/rojo-plugin-sync` will overwrite it to match the CLI.
   - If missing, mark MISSING.

7. **Check that `rojo` is reachable from the same shell `/rojo-serve` will use.** Run `which rojo` (or `where rojo` on Windows). Report the resolved path so PATH issues are visible.

**Output format:**

Print a table-like summary the user can scan quickly:

```
Rojo Dependency Health Check
============================
Platform:         <detected>
Rokit:            <status> (installed: <version>, latest: <version>)
Rojo CLI:         <status> (installed: <version>, pinned: 7.6.1)
rokit.toml:       <status> (project pin: <version or "none">)
Roblox Studio:    <status>
Studio plugin:    <status>
rojo on PATH:     <path or "not found">

Issues found: <count>
```

After the summary, list each issue with a one-line description and the exact slash command or manual step that fixes it. For example:
- "Rokit not installed → run `/rojo-setup` (will install via the official script)"
- "Roblox Studio not installed → download from https://www.roblox.com/create"
- "Rojo CLI is 7.5.1 but pinned to 7.6.1 → run `/rojo-setup` to update"

End with a single-line recommendation: either "All good — no action needed" or "Run `/rojo-setup` to fix N issues automatically".

Do NOT execute any installation steps in this command. Read-only.
