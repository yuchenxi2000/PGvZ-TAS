# PGvZ-TAS

Tool-Assisted Superplay framework and cheat mod for "PlantGirls vs. Zombies" (PGvZ).

## Required workflow

### Versioning and changelog

The mod has its own version number and supports only the latest game versions declared in `pgvz/version.py`; do not add backward-compatibility paths for older game versions.

- At the start of a change, inspect the working tree, `pgvz/version.py`, and the top of `CHANGELOG.md` to determine whether an unreleased version is already in progress.
- Every completed project change must be recorded in `CHANGELOG.md` under the current in-progress version.
- If there were no pre-existing project changes and no in-progress version, increment `MOD_VERSION` in `pgvz/version.py` first, then create a new top-level `CHANGELOG.md` section for that version and the current date.
- If pre-existing changes have already incremented the version and created its changelog section, add new entries to that same version instead of incrementing it again.
- Never add new changes beneath a previously released or otherwise old version heading.

### Documentation and reverse engineering

- Before decompiling the game, search `docs/` and `typings/`; the relevant behavior may already be documented.
- Record durable discoveries about game internals in a focused Chinese document under `docs/`, one topic per file. Keep this file limited to agent workflow, constraints, and navigation.
- Use the locally configured decompiled game source when implementation depends on current game internals. If its location is unavailable, ask the user.

## Source map and loading

| Path | Purpose |
|---|---|
| `pgvz/` | TAS framework: scripts, time operations, cards, cobs, utilities, and the two framework update hooks in `pgvz/__init__.py` |
| `pgvztool/` | Cheat mod; state and actions in `cheat.py`, placement in `placer.py`, synchronization in `sync.py`, TAS in `tas.py`, and cheat hooks in `hook.py` |
| `gui/` | Static Vue 3 + Element Plus GUI with no build step: layout in `index.html`, styles in `styles.css`, and behavior/protocol/data/i18n in `js/` |
| `cheat-gui.py` | Auto-loaded mod entry point that only configures paths and serves `gui/` on `localhost:58080` |
| `scripts/` | Example TAS scripts |
| `typings/` | Editor-only game and .NET type stubs |
| `tests/` | CPython unit tests for framework logic that can run outside the game |

The game scans only top-level `mods/*.py` files. Package directories are not auto-loaded. `cheat-gui.py` starts the HTTP server during game startup; `pgvz` and `pgvztool` are imported later by the WebSocket bootstrap in `gui/js/protocol.js` when a GUI connects. See [installation and loading](docs/install.md) and the [GUI protocol](docs/cheat-gui-protocol.md).

## Implementation constraints

- Runtime code must remain compatible with IronPython. Use `none_of(EnumType)` for C# enum members named `None`, quote modern annotations such as `'list[int]'`, and access game objects on the main game thread. See [IronPython and hooking notes](docs/scripting.md#5-ironpython-与-net-注意事项).
- Put cheat-mod `@HookTo` functions in `pgvztool/hook.py`. The framework driver hooks in `pgvz/__init__.py` are the intentional exception. Before changing a hook, inspect the current decompiled caller and the [hooking guide](docs/scripting.md#6-挂钩游戏方法); small methods may be inlined.
- Before changing overlays or coordinate conversions, read [the rendering and coordinate-system document](docs/rendering.md).
- Before changing WebSocket messages, client sessions, synchronization, persistence, or cheat toggles, read [the GUI protocol](docs/cheat-gui-protocol.md). Keep all user-facing option labels in both Chinese and English.
- Before changing script scheduling or time operations, read [the scripting guide](docs/scripting.md) and, where relevant, [the zombie-spawning timing document](docs/zombie-spawning.md).
- Before changing global or Board-local speed control, read [the speed-control document](docs/speed-control.md).
- Before changing TAS save/undo/redo behavior, read [the TAS document](docs/tas.md).
