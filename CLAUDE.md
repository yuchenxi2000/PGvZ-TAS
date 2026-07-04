# PGvZ-TAS

Tool-Assisted Superplay framework and cheat mod for "PlantGirls vs. Zombies" (PGvZ).

## Versioning

The mod has its own version number independent of the game. It always targets the **latest** game version only — older game versions are not supported.

## Architecture

```
pgvz/            TAS framework: time operations, card/plant management, cob manager, script scheduler
    ↑
pgvztool/        Cheat mod: all @HookTo functions in hook.py; logic in cheat.py, placer.py
    ↑
gui/             Single-page Vue3 + ElementPlus app controlling toggles over WebSocket
cheat-gui.py     Embedded HTTP server on localhost:58080; serves gui/ to browser
```

**Mod loading**: Game auto-scans `mods/` for `*.py` files on startup. Python packages (directories) are NOT auto-loaded — `pgvz` and `pgvztool` are imported by `cheat-gui.py` on startup, outside the main-thread timeout window.

**Communication**: Browser ↔ `cheat-gui.py` HTTP ↔ WebSocket `ws://localhost:8080/Py` ↔ in-game IronPython engine.

## Tech stack

- **Game engine**: C# / MonoGame
- **Mod language**: IronPython
- **Hooking**: `LawnMod.MonoModUtils.HookTo` decorator (wraps MonoMod.RuntimeDetour). Hooks register at module import time.
- **GUI**: Single HTML file, Vue3 + ElementPlus from CDN, no build step.
- **Top-level objects**: `Sexy.GlobalStaticVars.gLawnApp` → `GetLawnApp()`, `GetBoard()`

## Hooks

All `@HookTo` functions are in **`pgvztool/hook.py`**. `pgvztool/__init__.py` imports `cheat` → `placer` → `sync` → `hook`, so all dependencies are available when hooks register.

| File | Purpose |
|---|---|
| `pgvztool/cheat.py` | `CheatOption` class (all toggle state), script singletons |
| `pgvztool/placer.py` | `Placer` class (easy-place state and placement methods) |
| `pgvztool/hook.py` | All `@HookTo` functions |
| `pgvztool/sync.py` | `Serializable`, `SyncRegistry` — state sync |

`pgvz/__init__.py` also has two hooks (`LawnApp.UpdateFrames`, `Board.UpdateGame`) to drive `script_manager`.

If a hook on a small method seems to have no effect, the method may have been inlined by the runtime. Hooking a larger caller method instead typically resolves this.

## Coordinate systems & drawing hooks

The game has three coordinate systems (screen, board/world, grid) connected by camera transforms. The rendering pipeline has distinct hook levels; `Board.Draw` is the recommended level for overlay UI.

See [docs/rendering.md](docs/rendering.md) for full details.

## IronPython gotchas

- **C# enum `None` members**: Conflicts with Python keyword. Use `none_of(enum_type)` from `pgvz/util.py` (reflects via `getattr`).
- **Type annotations**: IronPython cannot handle annotations like `list[int]` or `tuple[int, int]` (tries to resolve them as .NET generics). Wrap them in quotes: `'list[int]'`, `'tuple[int, int]'`.
- **WebSocket JSON**: JSON booleans (`true`/`false`) are not valid Python. When sending JSON over WebSocket to be parsed by `json.loads()`, always wrap it as a Python string literal (single quotes). The receiver side must strip outer quotes before `JSON.parse()` — the `repr()` response from the WebSocket wraps the result in quotes.

## Script framework (pgvz)

- Scripts register via `script_manager.Register(func, runmode=ScriptRunMode.FOREVER)`. Blocking scripts use generator functions (containing `yield`).
- `Board.UpdateGame` hook calls `script_manager.Manage()` **before** each game tick.
- Acceleration: `GlobalStaticVars.gFastMo` (global, persists across levels) vs `Board.mAccelerationNumerator` (Board-local, dies with Board). In-game speed button uses the latter; cheat `SetSpeed` uses the former.

## Adding a new cheat toggle

See [docs/cheat-gui-protocol.md](docs/cheat-gui-protocol.md) for the full communication protocol and step-by-step guide.

## Decompiled code & docs

The decompiled game code reference path should be configured locally (check agent config, or ask the user).

When you discover a game internals detail worth recording (rendering, coordinate transforms, game mechanics, data structures), write a doc in `docs/` (in Chinese, one topic per file). Before decompiling to answer a question, check `docs/` first — it may have already been covered.
