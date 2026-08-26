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

可以重新绑定选择种子包、铲子、手套、轻松放置、TAS 按钮、暂停、加速和玉米炮等快捷键。
在 user_config.json 同级目录新建 keybinds.txt，每行填写一个“功能名 = 按键”，例如：

seed_1 = Q
pause = Enter

修改后需重启游戏，并打开网页连接修改器后才能生效。
已适配中文等常见非英文输入法下的字母和数字快捷键，桌面版还会自动关闭输入法选词框。
完整配置说明：https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/keybinds.md

===== 常见问题排查 =====

1. 打不开 http://localhost:58080
   确认游戏正在运行，安装或替换文件后已经完全重启游戏。
   确认地址是 http://localhost:58080，注意是 http 而不是 https，冒号是英文冒号。
   PC 用户请打开和 mods 同级的 user_config.json，确保 ironpython_enabled 为 true；手机用户不要做这一步，没这个文件是正常的。
   确认 mods 文件夹顶层存在且只存在一个作为入口使用的 cheat-gui.py；备份文件不要保留 .py 扩展名。
   Android 应使用同一台手机内的浏览器访问；PC 用户也应使用本机浏览器访问。
   Android 上可尝试重新解压并复制，必要时更换文件管理器。
   仍然打不开时，按下方“使用调试入口”操作，重点查看 HTTP 状态。

2. 网页打开了，但显示连接失败
   确认只打开了一个修改器页面。
   检查防火墙、代理、VPN 或浏览器安全设置是否拦截本机 WebSocket。
   8080 端口可能被占用，可以依次尝试：
   http://localhost:58080/?ws=ws://localhost:8081/Py
   http://localhost:58080/?ws=ws://localhost:8082/Py
   http://localhost:58080/?ws=ws://localhost:8083/Py
   仍然无法连接时，按下方“使用调试入口”操作，以诊断信息显示的 WebSocket 实际端口为准。

3. 网页空白或内容缺失
   检查 gui 文件夹内文件的完整性。完全退出游戏，删除 mods 中的旧 gui 目录，再从同一发布包重新复制；不要只覆盖旧目录。随后重新打开网页。
   仍有内容缺失时，按下方“使用调试入口”操作，重点查看 gui 文件检查结果。

4. 按钮没有效果
   先确认网页显示“已连接到游戏服务器”；否则按第 2 项排查 WebSocket 端口和连接状态。
   安装或替换入口和 Python 包后必须完全重启游戏，只刷新网页不会重新加载 Python 文件。
   确认 pgvz 和 pgvztool 来自同一发布包。完全退出游戏，删除这两个旧目录后重新复制；如果网页执行结果显示包导入异常，也应先重新复制它们。
   仍然无效时，按下方“使用调试入口”操作，重点查看 pgvz 和 pgvztool 文件检查结果。若文件检查为 OK，请保留网页“执行结果”中的完整异常信息。

5. 安卓上启动黑屏或闪退
   如果同时安装了很多模组，游戏初始化时可能加载太慢。可以先移除其他模组，只保留本修改器再试。

6. 文件复制后仍然异常
   请重新解压并复制。某些安卓文件管理器在解压或覆盖复制时可能漏文件。
   仍然异常时，按下方“使用调试入口”操作，查看 pgvz、pgvztool 和 gui 文件检查结果。

7. 自定义快捷键无效
   修改 keybinds.txt 后请重启游戏，并打开网页连接修改器。
   本修改器已适配常见非英文输入法；如果当前输入法仍然拦截快捷键，请切换到英文输入法后再试。

8. 提示“另一个修改器页面已连接”
   同时只使用一个修改器网页。后打开的页面会被拒绝，请关闭当前页面，继续使用先前页面。
   如果只看见一个页面，请关闭浏览器中所有修改器标签页和窗口，等待最多 15 秒，再只打开一个 http://localhost:58080 页面。或者尝试刷新页面。
   不要通过 file:// 直接打开 gui/index.html；它不会获得本地服务器提供的缓存控制响应头。

9. 修改器显示的状态与游戏内不一致
   先检查是否还开启了其他修改器、调试工具或游戏内置修改器。
   不同修改器可能各自修改同一个游戏变量，后执行的修改会改变游戏内的实际状态。各修改器界面通常只记录自己最后设置或同步到的值，不会实时感知其他入口所做的修改，因此界面显示可能仍是旧值。
   本修改器的单客户端保护只防止多个官方网页同时控制游戏，不会限制其他修改器或游戏内置修改器。

===== 使用调试入口 =====

调试入口适合区分入口未加载、HTTP 绑定失败、WebSocket 实际端口异常和安装文件缺失。它不会修复问题，也不能用于正式游玩。

使用方法：
1. 完全退出游戏，备份 mods 目录中的正式 cheat-gui.py：移出目录或者改后缀名。
2. 将发布包 debug 目录中的 cheat-gui.py 复制到 mods 目录并覆盖正式入口。正式和调试 cheat-gui.py 入口只能保留一个；备份文件应放到其他目录，或改成不以 .py 结尾。
3. 启动游戏。游戏资源加载完成并进入主界面时会显示诊断弹窗。
4. 弹窗显示 HTTP 状态、WebSocket 实际端口以及 pgvz、pgvztool、gui 文件检查结果。弹窗打开时也可以访问网页测试。
5. 同样的诊断信息也会写入 mods/pgvztool-debug-report.txt。正常情况下，弹窗和报告应当同时存在。
6. 记录诊断信息后退出游戏，按照诊断信息排查错误。
7. 错误排查完毕，修改器可正常使用后，恢复正式 cheat-gui.py。确认正式入口已经恢复后，可以删除 pgvztool-debug-report.txt。

根据诊断信息处理：

1. 没有弹窗，也没有 pgvztool-debug-report.txt
   调试入口没有执行。确认文件位于正确的 mods 目录、文件名为 cheat-gui.py，并重新复制调试脚本。PC 用户还应确认 user_config.json 中的 ironpython_enabled 为 true；手机用户没有这个文件是正常的。

2. 弹窗和 pgvztool-debug-report.txt 只出现其中一个
   调试入口发生内部错误。保留现有的弹窗内容或报告文件，并连同游戏版本、系统和设备信息提交给项目开发者。

3. HTTP 58080: OK，但网页仍打不开
   HTTP 服务本身已启动。确认使用 http://localhost:58080。Android 要在同一手机或模拟器的浏览器中访问。随后检查防火墙、代理、VPN、浏览器安全设置和本机网络环境。

4. HTTP 58080: 失败（…）
   根据括号内异常排查。端口占用时关闭其他游戏实例、本地服务和重复的 .py 入口后重启；权限或网络异常时检查安全软件和系统网络限制。

5. WebSocket 端口: N
   用 http://localhost:58080/?ws=ws://localhost:N/Py 访问，其中 N 替换为显示的实际端口。仍失败时检查防火墙、代理、VPN 和浏览器 WebSocket 限制。

6. WebSocket: 读取失败（…）
   先确认使用受支持的最新游戏版本并重新复制调试脚本。若仍出现，保留完整异常信息；这通常表示游戏内部类型或字段与调试入口不匹配，需要提交给项目维护者分析。

7. 文件检查：OK
   三个组件的关键文件均存在。若页面或按钮仍异常，恢复正式入口后重试，并保留网页“执行结果”中的完整异常。OK 不代表每个文件的内容一定未损坏。

8. pgvz 或 pgvztool 目录/文件缺失
   完全退出游戏，删除 mods 中对应旧目录，再从同一发布包完整复制；不要覆盖旧目录。两个包必须来自同一发布包。

9. gui 目录/文件缺失或 index.html 读取失败
   完全退出游戏，删除旧 gui 目录后从同一发布包完整复制。Android 上必要时重新解压或更换文件管理器。

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

You can rebind seed packet selection, shovel, glove, quick place, TAS actions, pause, acceleration, cob cannons, and other shortcuts.
Create keybinds.txt next to user_config.json and add one "action = key" entry per line, for example:

seed_1 = Q
pause = Enter

Restart the game after editing the file, then open and connect the web console to load the keybinds.
Letter and number shortcuts support common non-English input methods. On desktop, IME candidate windows are also dismissed automatically.
Full configuration guide: https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/keybinds.md

===== Troubleshooting =====

1. Cannot open http://localhost:58080
   Make sure the game is running and was fully restarted after installation or file replacement.
   Make sure the address is http://localhost:58080, using http rather than https and an English colon.
   On PC, open user_config.json next to the mods folder and make sure ironpython_enabled is true. Mobile users normally do not have this file and should skip this step.
   Make sure there is exactly one active cheat-gui.py entry in the top level of the mods folder. A backup must not retain the .py extension.
   On Android, use a browser on the same phone. On PC, use a browser on the same computer.
   On Android, extract and copy the package again, using another file manager if necessary.
   If the page still cannot open, follow “Using the Debug Entry” below and inspect the HTTP status.

2. Page opens but connection fails
   Make sure only one mod page is open.
   Check whether a firewall, proxy, VPN, or browser security setting blocks local WebSocket connections.
   Port 8080 may be occupied. Try:
   http://localhost:58080/?ws=ws://localhost:8081/Py
   http://localhost:58080/?ws=ws://localhost:8082/Py
   http://localhost:58080/?ws=ws://localhost:8083/Py
   If connection still fails, follow “Using the Debug Entry” below and use the actual WebSocket port shown by the diagnostic.

3. The page is blank or missing content
   Check that the files in the gui folder are complete. Fully exit the game, delete the old gui directory from mods, and copy it again from the same release package instead of overwriting it. Then reopen the page.
   If content is still missing, follow “Using the Debug Entry” below and inspect the gui file check.

4. Buttons do nothing
   First confirm that the page says it is connected to the game server. Otherwise, troubleshoot the WebSocket port and connection state in item 2.
   Fully restart the game after installing or replacing the entry and Python packages. Refreshing the page does not reload Python files in the game.
   Make sure pgvz and pgvztool came from the same release package. Fully exit the game, delete both old directories, and copy them again. If the page reports a package-import error, recopy these directories first.
   If buttons still do nothing, follow “Using the Debug Entry” below and inspect the pgvz and pgvztool file checks. If the check says OK, preserve the complete error shown in the page's execution result.

5. Android black screen or crash on startup
   Too many mods can slow down initialization. Try removing other mods and keeping only this tool.

6. Still broken after copying files
   Extract and copy again. Some Android file managers may skip or damage files during extraction or overwrite.
   If the problem remains, follow “Using the Debug Entry” below and inspect the pgvz, pgvztool, and gui file checks.

7. Custom keybinds do not work
   Restart the game after editing keybinds.txt, then open and connect the web console.
   Common non-English input methods are supported. If the current input method still intercepts shortcuts, switch to an English input method and try again.

8. The page says another mod page is connected
   Use only one mod web page at a time. A later page is rejected; close it and continue using the page that was opened first.
   If only one page is visible, close every tab or window showing the mod page, wait up to 15 seconds, then open only one http://localhost:58080 page. You can also try refreshing the page.
   Do not open gui/index.html through file:// because it does not receive the local server's cache-control headers.

9. A mod's displayed state does not match the game
   First check whether another mod, debugging tool, or the game's built-in cheat controls are enabled.
   Different modifiers may independently change the same game variable, and the last change determines the actual in-game state. Each interface usually remembers only the value it last set or synchronized and does not observe changes made through another control path in real time, so it may continue to display an older value.
   This tool's single-client protection only prevents multiple official web pages from controlling the game at once; it does not restrict other mods or the game's built-in cheat controls.

===== Using the Debug Entry =====

The debug entry distinguishes an entry that did not load, HTTP binding failures, the actual WebSocket port, and missing installation files. It does not repair problems and must not be used for normal play.

How to use it:
1. Fully exit the game and back up the regular cheat-gui.py from the mods folder by moving it elsewhere or changing its extension.
2. Copy cheat-gui.py from the release package's debug folder into mods, replacing the regular entry. Keep only one regular-or-debug cheat-gui.py entry; move the backup elsewhere or remove its .py extension.
3. Start the game. The diagnostic dialog appears after resources finish loading and the main menu opens.
4. The dialog shows HTTP status, the actual WebSocket port, and file checks for pgvz, pgvztool, and gui. You may test the page while the dialog is open.
5. The same diagnostic information is written to mods/pgvztool-debug-report.txt. Under normal operation, both the dialog and report should exist.
6. Record the diagnostic information, exit the game, and troubleshoot the reported errors.
7. After the errors are resolved and the tool works normally, restore the regular cheat-gui.py. After confirming the regular entry is restored, you may delete pgvztool-debug-report.txt.

How to handle each diagnostic:

1. No dialog and no pgvztool-debug-report.txt
   The debug entry did not execute. Confirm that it is in the correct mods folder, is named cheat-gui.py, and then copy the debug script again. PC users should also confirm that ironpython_enabled is true in user_config.json; mobile users normally do not have this file.

2. Only one of the dialog and pgvztool-debug-report.txt exists
   The debug entry encountered an internal error. Preserve the available dialog contents or report file and send it to the project developer together with the game version, operating system, and device information.

3. HTTP 58080: OK, but the page cannot open
   The HTTP service is running. Confirm that you use http://localhost:58080. On Android, use a browser on the same phone. Then check the firewall, proxy, VPN, browser security settings, and local network environment.

4. HTTP 58080: 失败（...） (HTTP failed)
   Use the exception in parentheses to diagnose it. For an occupied port, close other game instances, local services, and duplicate .py entries, then restart. For permission or network errors, check security software and system network restrictions.

5. WebSocket 端口: N (WebSocket port)
   Open http://localhost:58080/?ws=ws://localhost:N/Py, replacing N with the displayed port. If it still fails, check the firewall, proxy, VPN, and browser WebSocket restrictions.

6. WebSocket: 读取失败（...） (WebSocket read failed)
   Confirm that the latest supported game version is installed and copy the debug script again. If the error remains, preserve the complete exception. It usually means the game's internal type or field no longer matches the debug entry and should be reported to the project maintainer.

7. 文件检查：OK (File check: OK)
   The key files for all three components exist. If the page or buttons still fail, restore the regular entry and retry, preserving the complete error in the page's execution result. OK does not guarantee that every file's contents are undamaged.

8. pgvz or pgvztool reports 目录缺失/缺 (missing directory/file)
   Fully exit the game, delete the corresponding old directory from mods, and copy it completely from the same release package instead of overwriting it. Both packages must come from the same release.

9. gui reports 目录缺失/缺 or index.html 读取失败 (missing/read failure)
   Fully exit the game, delete the old gui directory, and copy it completely from the same release package. On Android, extract again or use another file manager if necessary.

===== Source and License =====

Source: https://github.com/yuchenxi2000/PGvZ-TAS
License: MIT License

===== Credits =====

Lineup data comes from PvZToolkit. Thanks to lmintlcx.
This project's lineup-code format is compatible with PvZToolkit, but compatibility with other tools is not guaranteed.
