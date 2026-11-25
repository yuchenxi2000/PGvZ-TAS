PGvZTool v{{MOD_VERSION}} for PGvZ v{{GAME_VERSION}}
使用方法 README

本压缩包已经内置 Vue {{VUE_VERSION}} 和 Element Plus {{ELEMENT_PLUS_VERSION}}。
网页控制台不需要联网也可以打开和使用。
安装前请确认游戏版本是 v{{GAME_VERSION}}。

===== PC 安装 =====

安装或升级前请完全退出游戏。升级时先备份自己修改过的文件。

方法一：自动安装
1. 解压本压缩包。
2. 双击运行 cp-cheat-mods.bat。
3. 启动游戏。
4. 在浏览器打开 http://localhost:58080

方法二：手动安装
1. 打开 mods 目录：
   C:\Users\{用户名}\AppData\Roaming\ZBC\PlantGirlsVsZombies\mods
   将 {用户名} 替换为 C:\Users 下当前 Windows 账户的文件夹名。AppData 默认隐藏，可将完整路径粘贴到文件资源管理器地址栏打开。
2. 升级时先移除旧版的 pgvz/、pgvztool/、gui/ 和 cheat-gui.py。若仍有旧版 cheat.py，也请移出 mods 或改成以 .disabled 结尾。
3. 把解压目录中的这些文件和文件夹复制进去：
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
4. 启动游戏。
5. 在本机浏览器打开 http://localhost:58080

===== 安卓安装 =====

1. 完全退出游戏并解压本压缩包。
2. 用文件管理器打开 mods 目录：
   /storage/emulated/0/Android/data/net.pvz.pgvz.zbcteam/files/mods
3. 升级时先备份自己修改过的文件，并移除旧版的 pgvz/、pgvztool/、gui/、cheat-gui.py 和 cheat.py。
4. 把解压目录中的这些文件和文件夹复制到 mods 目录：
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
5. 启动游戏，在同一台设备的浏览器打开 http://localhost:58080。

===== 使用提示 =====

1. 启动游戏后打开网页，等页眉显示「可操作」再使用普通功能。
2. 点击「基础」「场地」「关卡与显示」「出怪与布阵」「地形」或「调试」切换功能页。页眉的语言选项可在中文和英文之间切换。
3. 在「地形」页点击「读取当前地形」，再选择画笔，点击格子或拖动矩形编辑草稿。点击「实施修改」时，背景、6×9 格子与六行类型会写入当时的关卡。
4. 同一设备可在多个标签页或浏览器打开网页。后打开的页面会读取游戏当前状态，已连接的页面共享设置更新。
5. 安装或使用遇到问题时，可参看下方的常见问题排查和调试入口说明。

===== 场地放置 =====

1. 在“场地”页选择植物、僵尸、场地物品、掉落物等类型。
2. 选择行列和其他属性。
3. 在「场地放置」或「场地移除」卡片点击对应按钮。

===== 轻松放置 =====

1. 在「场地」页的「对象选择」卡片打开「启用轻松放置」。
2. 设置「轻松放置模式」和要放置的对象。
3. 进入关卡后点击游戏里的玉米饼（Taco）图标。铲子和手套同时显示时，图标在菜单右侧。
4. PC：左键放置，右键退出轻松放置。
5. 安卓：点按场地放置，再次点击玉米饼图标退出。
6. 在传送门关卡使用传送门模式时，先点击要移动的传送门，再点击可放置的空格子。

===== TAS 工具 =====

在「基础」页的「常用修改」中打开「启用 TAS」。进入支持的关卡后，游戏右下角会出现以下按钮。

Save：保存当前游戏状态
Undo：回到上一个保存点。从实时游玩状态第一次回退时，会先保存当前状态。
Redo：前进到下一个保存点
Adv：逐帧，运行一帧后暂停

右下角还会显示 Frame 计数器，可用于精确控制操作时机。

===== 自定义快捷键 =====

可以重新绑定选择种子包、铲子、手套、轻松放置、TAS 按钮、暂停、加速和玉米炮等快捷键。
在 mods 目录的上一级新建 keybinds.txt，每行填写一个「功能名 = 按键」，例如：

seed_1 = Q
pause = Enter

修改后重启游戏应用该按键映射。
已适配中文等常见非英文输入法下的字母和数字快捷键，桌面版还会自动关闭输入法选词框。
完整配置说明：https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/mod/user-guide/keybinds.md

===== 自定义代码 =====

在「调试」页的「输入 Python 代码」卡片输入代码，点击「发送代码」后，游戏会在 IronPython 环境中执行。结果显示在页面下方的「执行结果」。
「Python 调试端口」默认填 8080。游戏选用其他端口时，请在此填入实际端口。普通修改功能使用 58080。

脚本编写文档：https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/mod/user-guide/scripting.md
项目源码：https://github.com/yuchenxi2000/PGvZ-TAS

===== 常见问题排查 =====

1. 打不开 http://localhost:58080
   确认游戏正在运行，安装或替换文件后已经完全重启游戏。
   确认地址是 http://localhost:58080，注意是 http 而不是 https，冒号是英文冒号。
   PC 上如果在 mods 同级的 user_config.json 中看到了 "ironpython_enabled": false，请改为 true 后重启。未设置时，游戏默认启用 IronPython。
   确认 mods 文件夹顶层存在且只存在一个作为入口使用的 cheat-gui.py；备份文件不要保留 .py 扩展名。
   Android 应使用同一台手机内的浏览器访问；PC 用户也应使用本机浏览器访问。
   Android 上可尝试重新解压并复制，必要时更换文件管理器。
   仍然打不开时，按下方“使用调试入口”操作，重点查看 HTTP 状态。

2. 网页一直初始化、重连或显示「连接错误」
   显示「正在初始化修改器...」时，切回游戏等待加载完成，再回网页。
   显示「正在重连，3秒后重试...」时，确认游戏仍在运行。网页会自动尝试恢复连接。
   显示「连接错误」时，查看「执行结果」中的具体错误。打开 http://localhost:58080/api/status 也可检查后台加载结果，ready 为 false 表示还在加载，error 非空时可查看错误。
   显示「当前游戏版本不受支持」时，核对页眉的游戏版本和发布包标注的适用版本。
   若状态地址返回 404，请确认 cheat-gui.py、pgvz/、pgvztool/ 和 gui/ 来自同一发布包并重启游戏。

3. 网页空白或内容缺失
   检查 gui 文件夹是否完整。完全退出游戏，删除 mods 中的旧 gui 目录，再从同一发布包完整复制。启动游戏后刷新所有旧的修改器标签页。
   仍有内容缺失时，按下方“使用调试入口”操作，重点查看 gui 文件检查结果。

4. 按钮没有效果
   先确认页眉显示「可操作」。看到「已发送，切回游戏后生效」时，请切回游戏处理指令。看到「执行成功」时，游戏已返回结果。
   「速度控制」显示「等待游戏执行」时，也请切回游戏。
   如果网页提示部分指令的执行结果未确认，先回游戏检查是否生效，再决定是否重发。
   安装或替换入口和 Python 包后必须完全重启游戏，只刷新网页不会重新加载 Python 文件。
   确认 pgvz 和 pgvztool 来自同一发布包。完全退出游戏，删除这两个旧目录后重新复制；如果网页执行结果显示包导入异常，也应先重新复制它们。
   仍然无效时，按下方“使用调试入口”操作，重点查看 pgvz 和 pgvztool 文件检查结果。若文件检查为 OK，请保留网页“执行结果”中的完整异常信息。
   如果只有某项功能无法使用，请核对游戏版本是否与发布包匹配。问题仍存在时，可附上两项版本和完整错误，到 GitHub 提交 issue（https://github.com/yuchenxi2000/PGvZ-TAS/issues）。

5. 安卓上启动黑屏或闪退
   如果同时安装了很多模组，可以暂时移出其他顶层 .py 文件，保留本修改器的 cheat-gui.py、pgvz/、pgvztool/ 和 gui/ 后重试。

6. 文件复制后仍然异常
   请重新解压并复制。某些安卓文件管理器在解压或覆盖复制时可能漏文件。
   仍然异常时，按下方“使用调试入口”操作，查看 pgvz、pgvztool 和 gui 文件检查结果。

7. 自定义快捷键无效
   修改 keybinds.txt 后请重启游戏。
   本修改器已适配常见非英文输入法；如果当前输入法仍然拦截快捷键，请切换到英文输入法后再试。

8. 修改器显示的状态与游戏内不一致
   内置菜单的「自动收集资源」「房主无敌」「后台运行」会与网页同步，第一项在网页上显示为「自动收集」。
   内置菜单和网页各有一个「无冷却种植」开关。两个开关修改不同的游戏状态，互不同步。内置菜单会刷新冷却中的卡片，仍按原规则扣除阳光。网页开关会跳过卡片冷却检查，普通卡槽种植也会免除阳光消耗。
   网页「关卡与显示」的「全局速度」对应内置菜单的倍速。「关卡速度」只影响当前关卡的游戏逻辑。
   如果其他选项显示不一致，请检查是否还有其他模组或调试工具在修改同一设置。

===== 使用调试入口 =====

调试入口用于诊断 HTTP 服务和安装文件，并报告原生 Python 调试端口。

使用方法：
1. 完全退出游戏，备份 mods 目录中的正式 cheat-gui.py：移出目录或者改后缀名。
2. 将发布包 debug 目录中的 cheat-gui.py 复制到 mods 目录并覆盖正式入口。正式和调试 cheat-gui.py 入口只能保留一个；备份文件应放到其他目录，或改成不以 .py 结尾。
3. 启动游戏。游戏资源加载完成并进入主界面时会显示诊断弹窗。
4. 弹窗显示 HTTP 状态、Python 调试端口以及 pgvz、pgvztool、gui 文件检查结果。弹窗打开时也可以访问网页测试。
5. 同样的诊断信息也会写入 mods/pgvztool-debug-report.txt。正常情况下，弹窗和报告应当同时存在。
6. 记录诊断信息后退出游戏，按照诊断信息排查错误。
7. 错误排查完毕，修改器可正常使用后，恢复正式 cheat-gui.py。确认正式入口已经恢复后，可以删除 pgvztool-debug-report.txt。

根据诊断信息处理：

1. 没有弹窗，也没有 pgvztool-debug-report.txt
   先确认调试脚本已复制到正确的 mods 目录，文件名为 cheat-gui.py。PC 上还要确认没有在 user_config.json 中关闭 ironpython_enabled。

2. 弹窗和 pgvztool-debug-report.txt 只出现其中一个
   调试入口发生内部错误。保留现有的弹窗内容或报告文件，并连同游戏版本、系统和设备信息提交给项目开发者。

3. HTTP 58080: OK，但网页仍打不开
   HTTP 服务本身已启动。确认使用 http://localhost:58080。Android 要在同一手机或模拟器的浏览器中访问。随后检查防火墙、代理、VPN、浏览器安全设置和本机网络环境。

4. HTTP 58080: 失败（…）
   根据括号内异常排查。端口占用时关闭其他游戏实例、本地服务和重复的 .py 入口后重启；权限或网络异常时检查安全软件和系统网络限制。
   如果提示“仅静态文件，GUI API 加载失败”，重新复制同一发布包的 pgvztool/ 并重启。

5. Python 调试端口: N
   如果「发送代码」后显示「无法连接游戏的 Python 调试端口」，在「调试」页的「Python 调试端口」填入报告里的数字，再点击「发送代码」。

6. Python 调试端口: 读取失败（…）
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
Before installing, make sure your game version is v{{GAME_VERSION}}.

===== PC Installation =====

Fully exit the game before installing. Back up any files you changed before upgrading.

Option 1: automatic install
1. Extract this archive.
2. Double-click cp-cheat-mods.bat.
3. Start the game.
4. Open http://localhost:58080 in your browser.

Option 2: manual install
1. Open the mods folder:
   C:\Users\{username}\AppData\Roaming\ZBC\PlantGirlsVsZombies\mods
   Replace {username} with your Windows account folder name under C:\Users. AppData is hidden by default. Paste the full path into File Explorer’s address bar to open it.
2. When upgrading, remove the old pgvz/, pgvztool/, gui/, and cheat-gui.py. If you still have a legacy cheat.py, move it out of mods or give it a .disabled extension.
3. Copy these files and folders from the extracted package:
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
4. Start the game.
5. Open http://localhost:58080 in a browser on the same computer.

===== Android Installation =====

1. Fully exit the game and extract this archive.
2. Open the mods folder in your file manager:
   /storage/emulated/0/Android/data/net.pvz.pgvz.zbcteam/files/mods
3. When upgrading, back up any files you changed and remove the old pgvz/, pgvztool/, gui/, cheat-gui.py, and cheat.py.
4. Copy these files and folders from the extracted package:
   cheat-gui.py
   pgvz\
   pgvztool\
   gui\
5. Start the game and open http://localhost:58080 in a browser on the same device.

===== Usage Notes =====

1. Start the game, open the web console, and wait for the header to show “Ready” before using regular controls.
2. Use the Basics, Board, Stage & Display, Spawns & Lineup, Terrain, or Debug tab to switch features. The language selector in the header switches between Chinese and English.
3. In Terrain, click “Read Current Terrain,” choose a brush, then click cells or drag a rectangle to edit the draft. “Apply Changes” writes the background, 6×9 cell grid, and six row types to the level active when the command runs.
4. You can open the web console in multiple tabs or browsers on the same device. Each new page loads the current game state, and connected pages share setting updates.
5. For help with installation or usage, see Troubleshooting and Using the Debug Entry below.

===== Board Placement =====

1. Open the Board tab and choose plant, zombie, grid item, drop type, and other properties.
2. Choose row and column.
3. Click the corresponding button in the “Place” or “Remove” card.

===== Quick Place =====

1. In the Board tab’s “Object Selection” card, turn on “Enable Easy Place.”
2. Set “Easy Place Mode” and choose what to place.
3. Enter a level and click the Taco icon. When both the shovel and glove are visible, look to the right of the menu.
4. PC: left-click to place, right-click to exit.
5. Android: tap the board to place and tap the Taco icon again to exit.
6. In a portal level, use Portal mode to select a portal, then choose an empty cell where it can be placed.

===== TAS Tool =====

In the Basics tab, turn on “Enable TAS” in “Common Cheats.” In supported levels, four buttons appear in the lower-right corner.

Save: save the current game state
Undo: return to the previous save point. The first undo from live play saves the current state before going back.
Redo: move forward to the next save point
Adv: advance exactly one frame and pause

A Frame counter is also shown for frame-precise play.

===== Custom Keybinds =====

You can rebind seed packet selection, shovel, glove, quick place, TAS actions, pause, acceleration, cob cannons, and other shortcuts.
Create keybinds.txt in the parent directory of mods and add one "action = key" entry per line, for example:

seed_1 = Q
pause = Enter

Restart the game after editing the file. The mod reads the keybinds during background loading.
Letter and number shortcuts support common non-English input methods. On desktop, IME candidate windows are also dismissed automatically.
Full configuration guide: https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/mod/user-guide/keybinds.md

===== Custom Code =====

In the Debug tab’s “Python Code” card, enter code and click “Send Code” to run it in the game’s IronPython environment. The response appears under “Result” at the bottom of the page.
The “Python debug port” defaults to 8080. If the game uses another port, enter the actual port in that field. Regular controls use port 58080.

Scripting guide (Chinese): https://github.com/yuchenxi2000/PGvZ-TAS/blob/main/docs/mod/user-guide/scripting.md
Project source: https://github.com/yuchenxi2000/PGvZ-TAS

===== Troubleshooting =====

1. Cannot open http://localhost:58080
   Make sure the game is running and was fully restarted after installation or file replacement.
   Make sure the address is http://localhost:58080, using http rather than https and an English colon.
   On PC, if user_config.json next to mods contains "ironpython_enabled": false, change it to true and restart the game. The game enables IronPython by default when the setting is absent.
   Make sure there is exactly one active cheat-gui.py entry in the top level of the mods folder. A backup must not retain the .py extension.
   On Android, use a browser on the same phone. On PC, use a browser on the same computer.
   On Android, extract and copy the package again, using another file manager if necessary.
   If the page still cannot open, follow “Using the Debug Entry” below and inspect the HTTP status.

2. The page keeps initializing or reconnecting, or reports “Connection error”
   If the header shows “Initializing the mod...”, switch back to the game and let it finish loading, then return to the page.
   If it shows “Reconnecting, retrying in 3s...”, check that the game is still running. The page retries automatically.
   If it shows “Connection error”, check “Result” for the full error. You can also open http://localhost:58080/api/status. A ready value of false means loading is still in progress. The error field shows any loading error.
   If the page shows “Unsupported Game Version”, compare the game version in the header with the version supported by the release package.
   If the status URL returns 404, check that cheat-gui.py, pgvz/, pgvztool/, and gui/ all came from the same release, then restart the game.

3. The page is blank or missing content
   Check that the gui folder is complete. Fully exit the game, delete the old gui directory from mods, and copy it again from the same release package. After restarting the game, refresh all previously opened mod tabs.
   If content is still missing, follow “Using the Debug Entry” below and inspect the gui file check.

4. Buttons do nothing
   Check that the header shows “Ready”. If “Result” says “Sent. Takes effect when you switch back to the game”, return to the game so it can process the command. “Command completed” confirms that the game returned a result.
   If “Speed Control” shows “Waiting for the game”, return to the game to let the command run.
   If the page says command results are unconfirmed, check the game before sending those commands again.
   Fully restart the game after installing or replacing the entry and Python packages. Refreshing the page does not reload Python files in the game.
   Make sure pgvz and pgvztool came from the same release package. Fully exit the game, delete both old directories, and copy them again. If the page reports a package-import error, recopy these directories first.
   If buttons still do nothing, follow “Using the Debug Entry” below and inspect the pgvz and pgvztool file checks. If the check says OK, preserve the complete error shown in the page's execution result.
   If one feature does not work, check that the game version matches the release package. If the problem persists, report both versions and the full error at https://github.com/yuchenxi2000/PGvZ-TAS/issues.

5. Android black screen or crash on startup
   Too many mods can slow down initialization. Try removing other mods and keeping only this tool.

6. Still broken after copying files
   Extract and copy again. Some Android file managers may skip or damage files during extraction or overwrite.
   If the problem remains, follow “Using the Debug Entry” below and inspect the pgvz, pgvztool, and gui file checks.

7. Custom keybinds do not work
   Restart the game after editing keybinds.txt.
   Common non-English input methods are supported. If the current input method still intercepts shortcuts, switch to an English input method and try again.

8. The web console’s state does not match the game
   The built-in menu’s auto-collect, house invincibility, and background-run switches sync with “Auto Collect,” “House Invincible,” and “Run In Background” in the web console.
   The built-in “无冷却种植” switch and the web console’s “No Plant Cooldown” switch change different game settings and do not sync. The built-in switch refreshes cards on cooldown and keeps their usual sun costs. The web switch bypasses the cooldown check and waives sun costs when planting from regular seed slots.
   In Stage & Display, “Global Speed” corresponds to the built-in menu’s speed. “Level Speed” affects the current level’s game logic.
   If other settings differ, check whether another mod or debugging tool is changing the same setting.

===== Using the Debug Entry =====

The debug entry diagnoses the HTTP service and installation files and reports the game's Python debug port.

How to use it:
1. Fully exit the game and back up the regular cheat-gui.py from the mods folder by moving it elsewhere or changing its extension.
2. Copy cheat-gui.py from the release package's debug folder into mods, replacing the regular entry. Keep only one regular-or-debug cheat-gui.py entry; move the backup elsewhere or remove its .py extension.
3. Start the game. The diagnostic dialog appears after resources finish loading and the main menu opens.
4. The dialog shows HTTP status, the Python debug port, and file checks for pgvz, pgvztool, and gui. You may test the page while the dialog is open.
5. The same diagnostic information is written to mods/pgvztool-debug-report.txt. Under normal operation, both the dialog and report should exist.
6. Record the diagnostic information, exit the game, and troubleshoot the reported errors.
7. After the errors are resolved and the tool works normally, restore the regular cheat-gui.py. After confirming the regular entry is restored, you may delete pgvztool-debug-report.txt.

How to handle each diagnostic:

1. No dialog and no pgvztool-debug-report.txt
   Check that you copied the debug entry to the correct mods folder and named it cheat-gui.py. On PC, check that you have not disabled ironpython_enabled in user_config.json.

2. Only one of the dialog and pgvztool-debug-report.txt exists
   The debug entry encountered an internal error. Preserve the available dialog contents or report file and send it to the project developer together with the game version, operating system, and device information.

3. HTTP 58080: OK, but the page cannot open
   The HTTP service is running. Confirm that you use http://localhost:58080. On Android, use a browser on the same phone. Then check the firewall, proxy, VPN, browser security settings, and local network environment.

4. HTTP 58080: 失败（...） (HTTP failed)
   Use the exception in parentheses to diagnose it. For an occupied port, close other game instances, local services, and duplicate .py entries, then restart. For permission or network errors, check security software and system network restrictions.
   If the report says the GUI API failed to load, recopy pgvztool/ from the same release and restart the game.

5. Python 调试端口: N (Python debug port)
   If “Send Code” reports “Could not connect to the game’s Python debug port”, enter the number from the report in the Debug tab’s “Python debug port” field, then click “Send Code” again.

6. Python 调试端口: 读取失败（...） (Python debug port unavailable)
   Confirm that the latest supported game version is installed and copy the debug script again. If the error remains, preserve the complete exception. It usually means the game's internal type or field no longer matches the debug entry and should be reported to the project maintainer.

7. 文件检查：OK (File check: OK)
   The key files for all three components exist. If the page or buttons still fail, restore the regular entry and retry. Keep the complete message shown under “Result” for troubleshooting.

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
