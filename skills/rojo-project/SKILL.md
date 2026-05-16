---
name: rojo-project
description: Conventions, file naming, and project layout for Rojo-managed Roblox games. Use this skill whenever the user is editing Lua/Luau files in a Rojo project (presence of default.project.json or any *.project.json file), discussing Roblox services like ServerScriptService or ReplicatedStorage, working with init.lua / init.server.lua / init.client.lua files, asking how to add a new module/script/service, or troubleshooting sync issues between the file system and Roblox Studio.
---

# Working in a Rojo Project

**Pinned Rojo version for this plugin: 7.6.1.** If the user reports a version mismatch error in Studio, tell them to run `/rojo-plugin-sync` and restart Studio.

Rojo maps a folder tree on disk to a Roblox instance tree in Studio. The mapping is defined by `default.project.json` (or any `*.project.json` file). Understanding this mapping is essential before creating or moving files — putting a script in the wrong folder means it ends up in the wrong service in Studio and probably won't run.

## File-name suffixes determine instance class

Rojo decides what kind of Roblox instance a Lua file becomes based on its name suffix:

- `Foo.lua` or `Foo.luau` → `ModuleScript` named `Foo`
- `Foo.server.lua` or `Foo.server.luau` → `Script` (server-side) named `Foo`
- `Foo.client.lua` or `Foo.client.luau` → `LocalScript` named `Foo`

Inside a folder that represents an instance, the special name `init` becomes that folder itself:

- `Foo/init.lua` → the folder `Foo` becomes a `ModuleScript`
- `Foo/init.server.lua` → the folder `Foo` becomes a server `Script`
- `Foo/init.client.lua` → the folder `Foo` becomes a `LocalScript`

This is how you give a script children. A folder named `Combat` with `init.server.lua` plus other `.lua` files inside becomes a server Script with ModuleScript children.

## Read the project file before placing anything

Before creating a new file, read `default.project.json`. The `tree` field shows which on-disk path maps to which service. A typical layout:

```json
{
  "name": "MyGame",
  "tree": {
    "$className": "DataModel",
    "ServerScriptService": { "$path": "src/server" },
    "ReplicatedStorage": {
      "Shared": { "$path": "src/shared" }
    },
    "StarterPlayer": {
      "StarterPlayerScripts": { "$path": "src/client" }
    }
  }
}
```

With that config:
- A new server script goes in `src/server/` as `Whatever.server.lua`.
- A shared module goes in `src/shared/` as `Whatever.lua`.
- A client script goes in `src/client/` as `Whatever.client.lua`.

If the user asks for "a new module for X", figure out from the request whether it's server, client, or shared, then place it in the matching `$path`. If it's ambiguous, ask before creating.

## Common mistakes to avoid

- **Don't use `.lua` for a script that should run.** Plain `.lua` is a ModuleScript and won't execute on its own. Server scripts need `.server.lua`; client scripts need `.client.lua`.
- **Don't put server scripts in ReplicatedStorage.** They won't run there. Server code belongs in `ServerScriptService` or `ServerStorage`.
- **Don't put client scripts in ServerScriptService.** LocalScripts only run from places like `StarterPlayerScripts`, `StarterCharacterScripts`, `StarterGui`, or `ReplicatedFirst`.
- **Don't edit `.rbxlx`/`.rbxm` files directly when Rojo is managing the project.** They're build outputs. The source of truth is the file tree.
- **`require()` uses Roblox paths, not file paths.** `require(ReplicatedStorage.Shared.Foo)`, not `require("../shared/Foo")`.

## Sync workflow

Rojo only syncs while `rojo serve` is running and the user has clicked "Connect" in the Rojo Studio plugin. Edits made while the server is stopped are still saved to disk but won't appear in Studio until the next connection. If a file edit doesn't seem to be showing up in Studio, the most likely causes (in order) are: server not running, Studio plugin not connected, or file is in a path not covered by the project's `tree` mapping.

## Luau notes

Roblox uses Luau, not standard Lua. Key differences when writing code:
- Type annotations are allowed: `local function add(a: number, b: number): number`
- `task.wait`, `task.spawn`, `task.delay` are preferred over the deprecated globals.
- `string.split`, `table.find`, `table.clear` exist.
- No `goto`, no bitwise operators via `bit32` being deprecated (use built-in operators `//`, `&`, `|`, `~`, `<<`, `>>` where supported by your Luau version).
