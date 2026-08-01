PGvZTool v{{MOD_VERSION}} for PGvZ v{{GAME_VERSION}}
使用方法 README

本压缩包已经内置 Vue {{VUE_VERSION}} 和 Element Plus {{ELEMENT_PLUS_VERSION}}。
网页控制台不需要联网也可以打开和使用。

===== PC 安装 =====

方法一：自动安装
1. 解压本压缩包。
2. 双击运行 cp-cheat-mods.bat。
3. 启动或重启游戏。
4. 在浏览器打开 http://localhost:58080

方法二：手动安装
1. 打开 mods 目录：
   C:\Users\{用户名}\AppData\Roaming\ZBC\PlantGirlsVsZombies\mods
2. 把本目录下这些文件和文件夹复制进去：
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
3. 启动或重启游戏。
4. 在浏览器打开 http://localhost:58080

===== 安卓安装 =====

1. 解压本压缩包。
2. 用文件管理器把这些文件和文件夹复制到 mods 目录：
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
3. 安卓 mods 目录通常是：
   /storage/emulated/0/Android/data/net.pvz.pgvz.zbcteam/files/mods
4. 启动或重启游戏。
5. 在浏览器打开 http://localhost:58080

===== 使用提示 =====

1. 必须先启动游戏，再打开网页控制台。
2. 如果安装时游戏已经打开，请重启游戏后再使用。
3. 网页左上角显示“已连接到游戏服务器”后，按钮才会执行到游戏里。
4. 基础、场地、关卡、出怪与布阵、自定义代码都在网页上方标签页里。
5. 自定义代码会发送到游戏内 IronPython 环境执行，适合临时运行脚本或调试命令。

===== 场地放置 =====

1. 在“场地”页选择植物、僵尸、场地物品、掉落物等类型。
2. 选择行列和其他属性。
3. 点击对应按钮放置或移除。

===== 轻松放置 =====

1. 在“场地”页启用轻松放置。
2. 选择轻松放置模式：植物、僵尸、场地物品、掉落物、割草机、传送门等。
3. 进入关卡后点击游戏里铲子旁边的 Taco 图标。
4. PC：左键放置，右键退出轻松放置。
5. 安卓：再次点击 Taco 图标退出轻松放置。
6. 传送门模式可以移动传送门位置。

===== TAS 工具 =====

在“常用修改”中勾选“启用 TAS”后，游戏右下角会出现 TAS 按钮：

Save：保存当前游戏状态
Undo：回到上一个保存点
Redo：前进到下一个保存点
Adv：逐帧，运行一帧后暂停

右下角还会显示 Frame 计数器，可用于精确控制操作时机。

===== 自定义快捷键 =====

可以重新绑定选择种子包、使用铲子、暂停、加速和玉米炮等快捷键。
在 user_config.json 同级目录新建 keybinds.txt，每行填写一个“功能名 = 按键”，例如：

seed_1 = Q
pause = Enter

修改后需重启游戏，并打开网页连接修改器后才能生效。
已适配中文等常见非英文输入法下的字母和数字快捷键，桌面版还会自动关闭输入法选词框。
完整配置说明：https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/keybinds.md

===== 常见问题排查 =====

1. 打不开 http://localhost:58080
   请确认游戏已经启动，并且 cheat-gui.py 已经放在 mods 目录下。

2. 网页打开了，但显示连接失败
   可能是 WebSocket 端口不是 8080。可以依次尝试：
   http://localhost:58080/?ws=ws://localhost:8081/Py
   http://localhost:58080/?ws=ws://localhost:8082/Py
   http://localhost:58080/?ws=ws://localhost:8083/Py

3. 按钮没有效果
   请先看网页连接状态是否为“已连接到游戏服务器”。如果不是，请重启游戏和浏览器页面。

4. 安卓上启动黑屏或闪退
   如果同时安装了很多模组，游戏初始化时可能加载太慢。可以先移除其他模组，只保留本修改器再试。

5. 文件复制后仍然异常
   请重新解压并复制。某些安卓文件管理器在解压或覆盖复制时可能漏文件。

6. 自定义快捷键无效
   修改 keybinds.txt 后请重启游戏，并打开网页连接修改器。
   本修改器已适配常见非英文输入法；如果当前输入法仍然拦截快捷键，请切换到英文输入法后再试。

===== 源码和许可证 =====

源码：https://github.com/yuchenxi2000/PGvZ-TAS
许可证：MIT License

===== 致谢 =====

布阵码数据来自 PvZToolkit，感谢 lmintlcx。
本项目布阵码格式和 PvZToolkit 兼容，不保证和其他项目兼容。


============================================================
English Guide
============================================================

PGvZTool v{{MOD_VERSION}} for PGvZ v{{GAME_VERSION}}

This release bundles Vue {{VUE_VERSION}} and Element Plus {{ELEMENT_PLUS_VERSION}} locally.
The web console works without an internet connection.

===== PC Installation =====

Option 1: automatic install
1. Extract this archive.
2. Double-click cp-cheat-mods.bat.
3. Start or restart the game.
4. Open http://localhost:58080 in your browser.

Option 2: manual install
1. Open the mods folder:
   C:\Users\{username}\AppData\Roaming\ZBC\PlantGirlsVsZombies\mods
2. Copy these files and folders into it:
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
3. Start or restart the game.
4. Open http://localhost:58080 in your browser.

===== Android Installation =====

1. Extract this archive.
2. Use a file manager to copy these files and folders into the mods folder:
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
3. The Android mods folder is usually:
   /storage/emulated/0/Android/data/net.pvz.pgvz.zbcteam/files/mods
4. Start or restart the game.
5. Open http://localhost:58080 in your browser.

===== Usage Notes =====

1. Start the game before opening the web console.
2. If the game was already running during installation, restart it.
3. Buttons only affect the game after the page shows that it is connected to the game server.
4. The top tabs contain Basics, Board, Stage, Spawns & Lineup, and Custom Code.
5. Custom Code is executed in the game's IronPython environment.

===== Board Placement =====

1. Open the Board tab and choose plant, zombie, grid item, drop type, and other properties.
2. Choose row and column.
3. Click the corresponding button to place or remove objects.

===== Quick Place =====

1. Enable Easy Place in the Board tab.
2. Choose an easy-place mode: plant, zombie, grid item, drop, mower, portal, and so on.
3. Enter a level and click the Taco icon next to the shovel in-game.
4. PC: left-click to place, right-click to exit.
5. Android: tap the Taco icon again to exit.
6. Portal mode can move portals.

===== TAS Tool =====

Enable TAS in Common Cheats. Four buttons appear in the lower-right corner:

Save: save the current game state
Undo: return to the previous save point
Redo: move forward to the next save point
Adv: advance exactly one frame and pause

A Frame counter is also shown for frame-precise play.

===== Custom Keybinds =====

You can rebind seed packet selection, shovel, pause, acceleration, cob cannons, and other shortcuts.
Create keybinds.txt next to user_config.json and add one "action = key" entry per line, for example:

seed_1 = Q
pause = Enter

Restart the game after editing the file, then open and connect the web console to load the keybinds.
Letter and number shortcuts support common non-English input methods. On desktop, IME candidate windows are also dismissed automatically.
Full configuration guide: https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/keybinds.md

===== Troubleshooting =====

1. Cannot open http://localhost:58080
   Make sure the game is running and cheat-gui.py is in the mods folder.

2. Page opens but connection fails
   The WebSocket port may not be 8080. Try:
   http://localhost:58080/?ws=ws://localhost:8081/Py
   http://localhost:58080/?ws=ws://localhost:8082/Py
   http://localhost:58080/?ws=ws://localhost:8083/Py

3. Buttons do nothing
   Check that the page says it is connected to the game server. If not, restart the game and refresh the page.

4. Android black screen or crash on startup
   Too many mods can slow down initialization. Try removing other mods and keeping only this tool.

5. Still broken after copying files
   Extract and copy again. Some Android file managers may skip or damage files during extraction or overwrite.

6. Custom keybinds do not work
   Restart the game after editing keybinds.txt, then open and connect the web console.
   Common non-English input methods are supported. If the current input method still intercepts shortcuts, switch to an English input method and try again.

===== Source and License =====

Source: https://github.com/yuchenxi2000/PGvZ-TAS
License: MIT License

===== Credits =====

Lineup data comes from PvZToolkit. Thanks to lmintlcx.
This project's lineup-code format is compatible with PvZToolkit, but compatibility with other tools is not guaranteed.
