---
description: Install/update the Roblox Studio plugin so it matches the CLI version
allowed-tools: Bash
---

Make sure the Rojo Studio plugin in Roblox Studio matches the version of the Rojo CLI on this machine. A version mismatch causes connection errors and sync failures.

Steps:
1. Verify `rojo` is on PATH: run `which rojo` (or `where rojo` on Windows). If not found, tell the user to install Rojo first and stop.
2. Print the current CLI version: `rojo --version`.
3. Run `rojo plugin install`. This command bundles the Studio plugin from the CLI binary and writes it as `RojoManagedPlugin.rbxm` into Roblox Studio's plugins folder, automatically. No paths needed.
4. If the command succeeds, tell the user:
   - The plugin is now version-matched with the CLI.
   - They need to restart Roblox Studio (or disable+re-enable the plugin) for Studio to pick up the new file.
   - If they previously installed the Rojo plugin from the Roblox marketplace, they should disable that version in Studio's plugin manager to avoid two Rojo plugins fighting.
5. If the command fails, show the error verbatim. Common causes:
   - Roblox Studio is not installed on this machine (CLI can't find the plugins folder).
   - Permission issue on the plugins folder.
   - Old `rojo` version that doesn't have the `plugin install` subcommand (added in Rojo 7.x; tell the user to upgrade).
