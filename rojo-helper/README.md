# rojo-helper

A Claude Code plugin for working on Roblox games managed by [Rojo](https://rojo.space).

**Pinned Rojo version: 7.6.1** (current stable). `/rojo-doctor` checks for it and `/rojo-setup` installs or updates to it.

## What you get

**Health & setup**
- `/rojo-doctor` — read-only health check. Reports what's installed, what's missing, what's out of date. Always safe to run.
- `/rojo-setup` — installs or updates Rokit, the Rojo CLI (pinned to 7.6.1), and the Studio plugin. Asks before making changes. Idempotent.
- `/rojo-plugin-sync` — re-installs the Studio plugin to match the current CLI version (use after upgrading the CLI manually).

**Day-to-day**
- `/rojo-serve` — start the Rojo sync server in the background
- `/rojo-stop` — stop the running server
- `/rojo-status` — show whether the server is running and tail recent logs
- `/rojo-build [output]` — build a `.rbxlx` from the project (defaults to `build.rbxlx`)

**Skill**
- `rojo-project` — auto-loads when Claude detects a Rojo project. Teaches Claude the `.server.lua` / `.client.lua` / `init.lua` naming conventions, how `default.project.json` maps folders to services, and common mistakes to avoid before placing files.

**Hook**
- A pre-edit hook prints a non-blocking warning if you edit files in a Rojo project while no server is running.

## Recommended first-run on a new machine

```
/rojo-doctor   # see what's missing
/rojo-setup    # install/update everything (will confirm each change)
/rojo-serve    # start syncing
```

On a clean machine that doesn't have Rokit yet, `/rojo-setup` will tell you the exact one-liner to install Rokit (it does NOT pipe `curl | bash` from inside the slash command — you run it yourself, then re-run `/rojo-setup`).

Roblox Studio itself is **not** installed by `/rojo-setup` — the Studio installer requires a Roblox account login. If Studio is missing, the doctor will say so and link you to https://www.roblox.com/create.

## How version-matching works

Every Rojo CLI binary has the Studio plugin baked into it. `rojo plugin install` (called by `/rojo-plugin-sync` and `/rojo-setup`) extracts that bundled plugin and writes it to Studio as `RojoManagedPlugin.rbxm`. So once the CLI is at the pinned version, the Studio plugin matches by construction.

If you see "plugin version doesn't match server version" in Studio's output: run `/rojo-plugin-sync` and restart Studio.

## Upgrading the pinned version

When a new stable Rojo is out (e.g., 7.7.0 leaves RC), edit two files:
- `commands/rojo-setup.md` — change the `7.6.1` references
- `commands/rojo-doctor.md` — change the `7.6.1` references
- `skills/rojo-project/SKILL.md` — change the version note at the top

Commit and push; users run `/plugin marketplace update`.

## Install (the Claude Code plugin itself)

### Option A: marketplace

```
/plugin marketplace add treeman0/claude-code-rojo
/plugin install rojo-helper@treeman0
```

### Option B: load locally

```
claude --plugin-dir /path/to/rojo-helper
```

### Option C: user plugins folder

```
cp -r rojo-helper ~/.claude/plugins/
```

## Requirements

- A working shell (`/rojo-setup` handles installing Rokit, then Rojo).
- Roblox Studio (installed manually from https://www.roblox.com/create).
- Network access for the first-time install steps.

## Notes

- `/rojo-serve` logs to `.rojo-server.log` (in the repo's `.gitignore`).
- The pre-edit hook only fires when a `*.project.json` is present in the working directory.
- Delete `hooks/` if you don't want the warning.
