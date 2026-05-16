---
description: Build the Rojo project to a place or model file
argument-hint: [output-file]
allowed-tools: Bash
---

Build the current Rojo project into a `.rbxlx` or `.rbxmx` file.

Arguments: `$ARGUMENTS` — optional output path. If not provided, default to `build.rbxlx` in the working directory.

Steps:
1. Find the project file (`default.project.json` preferred; otherwise ask the user which `*.project.json` to use).
2. Run `rojo build <project-file> --output <output>` where `<output>` is `$ARGUMENTS` or `build.rbxlx`.
3. If the build succeeds, report the output file path and its size (`ls -lh <output>`).
4. If it fails, show the error output verbatim.
