# rojo-helper

A Claude Code plugin for working on Roblox games managed by [Rojo](https://rojo.space).

## What you get

**Slash commands**
- `/rojo-serve` — start the Rojo sync server in the background
- `/rojo-stop` — stop the running server
- `/rojo-build [output]` — build a `.rbxlx` from the project (defaults to `build.rbxlx`)
- `/rojo-status` — show whether the server is running and tail recent logs

**Skill**
- `rojo-project` — auto-loads when Claude detects a Rojo project. Teaches Claude the `.server.lua` / `.client.lua` / `init.lua` naming conventions, how `default.project.json` maps folders to services, and common mistakes to avoid before it places files.

**Hook**
- A pre-edit hook that prints a friendly warning to stderr if you edit files in a Rojo project while no server is running. Non-blocking — edits still go through.

## Install

### Option A: load locally from disk

From your project directory, start Claude Code with the plugin path:

```
claude --plugin-dir /path/to/rojo-helper
```

### Option B: install via marketplace

1. Push this directory to a git repo.
2. In Claude Code, run `/plugin` and add the repo as a marketplace, then install `rojo-helper` from it.

### Option C: drop into your user plugins folder

```
cp -r rojo-helper ~/.claude/plugins/
```

## Requirements

- `rojo` on your `PATH` (`cargo install rojo` or grab a release from the repo).
- The Rojo Studio plugin installed in Roblox Studio (for the Studio side of the sync).

## Notes

- The `/rojo-serve` command logs to `.rojo-server.log` in the working directory. Add that to your `.gitignore`.
- The hook only fires inside directories that contain a `*.project.json` file, so it won't be noisy in non-Rojo projects.
- If you don't want the warning hook, delete the `hooks/` directory — everything else still works.
