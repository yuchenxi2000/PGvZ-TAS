# PGvZ-TAS

A scripting framework, cheat mod, and TAS tool for PlantGirls vs. Zombies (PGvZ). by yuchenxi2000

> [中文版本](README.md)

> PlantGirls vs. Zombies (PGvZ) is a community mod of Plants vs. Zombies by [庄不纯](https://space.bilibili.com/20530305)

## Quick Start

**PC**: Run `cp-cheat-mods.bat` for automatic installation, or manually copy `pgvz/`, `pgvztool/`, `gui/`, `cheat-gui.py` into the mods directory. Launch the game and open `http://localhost:58080` in your browser.

**Android**: Copy the above files into the mods directory, launch the game, and open `http://localhost:58080` in your browser. (You may need a file manager app such as MT Manager to copy files.)

Mods directory location:

| Platform | Path |
|---|---|
| PC | `C:\Users\{username}\AppData\Roaming\ZBC\PlantGirlsVsZombies\mods` |
| Android | `/storage/emulated/0/Android/data/net.pvz.pgvz.zbcteam/files/mods` |

See [docs/install.md](docs/install.md) (Chinese) for detailed installation steps and troubleshooting.

## Cheat Mod & TAS Tool

- **Common cheats**: Free plants, plant anywhere, plant/zombie invincibility, stop spawning, and dozens more toggles
- **Item placement**: Select plant/zombie/item types and properties in the web UI, then click to place them on the field
- **Quick place**: Check "轻松放置", choose a placement mode, click the Taco icon (to the right of the shovel) in-game to activate, left-click to place, right-click to exit
- **TAS tool**: Check "启用 TAS" in "常用修改". Four buttons appear in the bottom-right corner — Save, Undo (go back to previous save; auto-saves current state first when live), Redo (go forward to next save), Adv (advance one frame then pause). A frame counter is also displayed. Use these for frame-precise control, similar to emulator TAS tools
- **Custom keybinds**: Rebind seed packet selection, shovel, glove, quick place, TAS actions, pause and other keys. Common non-English input methods are supported. See [docs/keybinds.md](docs/keybinds.md)

Below is a visual guide for the quick-place and TAS features:

![Quick place and TAS tool](docs/PGvZTool_tips1.jpg)

## Scripting

The `pgvz` module provides a complete scripting framework including card selection, timing control, cob cannon management, and script scheduling. Scripts are written as generator functions and registered with `script_manager` to run alongside game frames.

See [docs/scripting.md](docs/scripting.md) (Chinese) for scripting guides and tutorials.

## License

MIT License

## Credits

Lineup data from PvZToolkit (thanks to lmintlcx).
